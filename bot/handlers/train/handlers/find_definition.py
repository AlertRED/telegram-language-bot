from datetime import timedelta
from random import shuffle

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from aiogram.utils.i18n import gettext as _
from rq import cancel_job

from bot.instances import (
    dispatcher as dp,
    bot,
)
from bot.instances import queue, redis
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.utils.browse_collection import start_browse
from bot.handlers.train.callbacks import FindDefinitionCallback
import database.dao as dao


class FindDefinitionStates(StatesGroup):
    choose_collection = State()
    try_guess = State()
    finished_train = State()


@dp.callback_query(FindDefinitionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(FindDefinitionStates.choose_collection)


@dp.callback_query(
    CollectionSelectCallback.filter(),
    FindDefinitionStates.choose_collection,
)
@dp.callback_query(
    CollectionSelectCallback.filter(),
    FindDefinitionStates.finished_train,
)
async def start_train(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
        wins_count=0,
        lose_count=0,
        used_term_ids=[],
        chat_id=callback.message.chat.id,
    )
    await callback.message.delete()
    await guess(state=state)
    await state.set_state(FindDefinitionStates.try_guess)


async def guess(
    state: FSMContext,
) -> None:
    LIMIT_OF_OPTIONS: int = 4
    state_data = await state.get_data()
    try:
        terms = dao.get_find_definition_terms(
            collection_id=state_data.get('collection_id'),
            excluded_ids=state_data.get('used_term_ids', []),
            limit=LIMIT_OF_OPTIONS,
        )
    except dao.NotEnoughTermsException:
        await finish_game(state)
        return

    correct_term = terms[0]

    used_term_ids = state_data.get('used_term_ids')
    used_term_ids.append(correct_term.id)
    await state.update_data(used_term_ids=used_term_ids)

    text = (f'{correct_term.name}')
    shuffle(terms)

    correct_option_id = terms.index(correct_term)
    await state.update_data(correct_option_id=correct_option_id)
    await bot.send_poll(
        chat_id=state.key.chat_id,
        question=text,
        is_anonymous=False,
        type='quiz',
        correct_option_id=correct_option_id,
        options=(
            [term.description for term in terms]
        ),
        open_period=10,
    )
    job = queue.enqueue_in(
        timedelta(seconds=10),
        time_was_expired,
        state.key.chat_id,
        state.key.user_id,
    )
    await state.update_data(job_expired_time_id=job.id)


async def time_was_expired(chat_id: int, user_id: int):
    await bot.send_message(
        chat_id=chat_id,
        text=_('Time was expired :('),
    )

    state: FSMContext = FSMContext(
        bot=bot,
        storage=dp.storage,
        key=StorageKey(
            chat_id=chat_id,
            user_id=user_id,
            bot_id=bot.id,
        ),
    )
    await state.update_data(job_expired_time_id=None)
    await continue_guessing(state, False)


async def continue_guessing(
    state: FSMContext,
    is_prev_won: bool,
):
    state_data = await state.get_data()
    job_expired_time_id = state_data.get('job_expired_time_id')
    if job_expired_time_id:
        cancel_job(job_id=job_expired_time_id, connection=redis)
    if is_prev_won:
        await state.update_data(
            wins_count=state_data.get('wins_count') + 1,
        )
    else:
        await state.update_data(
            lose_count=state_data.get('lose_count') + 1,
        )

    await guess(state=state)


@dp.poll_answer()
async def get_poll_answer(
    poll: types.PollAnswer,
    state: FSMContext,
):
    state_data = await state.get_data()
    await continue_guessing(
        state,
        state_data.get('correct_option_id') == poll.option_ids[0],
    )


async def finish_game(
    state: FSMContext,
):
    state_data = await state.get_data()
    wins_count = state_data.get('wins_count')
    lose_count = state_data.get('lose_count')
    chat_id = state_data.get('chat_id')

    accuracy = wins_count / ((wins_count + lose_count) or 1)

    await bot.send_message(
        chat_id=chat_id,
        text=_(
            'Wins: {wins_count} | Loses: {lose_count}'
            '\nAccuracy: {accuracy:.1%}'
        ).format(
            wins_count=wins_count,
            lose_count=lose_count,
            accuracy=accuracy,
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Try again'),
                        callback_data=CollectionSelectCallback(
                            collection_id=state_data.get('collection_id'),
                            collection_name=state_data.get('collection_name'),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.clear()
    await state.set_state(FindDefinitionStates.finished_train)
