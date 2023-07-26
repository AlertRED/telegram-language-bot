from random import shuffle

from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

from bot import bot
from bot.utils.calbacks import CollectionSelectCallback
from bot.utils.browse_collection import start_browse
from bot.train.callbacks import (
    FindDefinitionCallback,
    TryGuessCallback,
)
import database.dao as dao


router = Router()


class FindDefinitionStates(StatesGroup):
    choose_collection = State()
    try_guess = State()
    finished_train = State()


@router.callback_query(FindDefinitionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(FindDefinitionStates.choose_collection)


@router.callback_query(
    CollectionSelectCallback.filter(),
    FindDefinitionStates.choose_collection,
)
@router.callback_query(
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
    await guess(
        state=state,
        chat_id=callback.message.chat.id,
    )
    await state.set_state(FindDefinitionStates.try_guess)


@router.callback_query(
    TryGuessCallback.filter(),
    FindDefinitionStates.try_guess,
)
async def guess_again(
    callback: types.CallbackQuery,
    callback_data: TryGuessCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()

    used_term_ids = state_data.get('used_term_ids')
    used_term_ids.append(callback_data.right_term_id)
    await state.update_data(used_term_ids=used_term_ids)
    if (callback_data.previous_result):
        results = 'You won!🎉'
        await state.update_data(
            wins_count=state_data.get('wins_count') + 1,
        )
    else:
        await state.update_data(
            lose_count=state_data.get('lose_count') + 1,
        )
        term = dao.get_term(callback_data.right_term_id)
        results = (
            f'Wrong :(\n'
            f'<u><b>{term.name}</b></u>'
            f' - {term.description}'
        )

    await state.update_data(prev_results=results)
    await guess(
        chat_id=callback.message.chat.id,
        state=state,
    )


async def guess(
    state: FSMContext,
    chat_id: int,
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
    text = (f'{correct_term.name}')
    used_term_ids = state_data.get('used_term_ids')
    used_term_ids.append(correct_term.id)
    shuffle(terms)

    correct_option_id = terms.index(correct_term)
    await state.update_data(correct_option_id=correct_option_id)
    await bot.send_poll(
        chat_id=chat_id,
        question=text,
        is_anonymous=False,
        type='quiz',
        correct_option_id=correct_option_id,
        options=(
            [term.description for term in terms]
        ),
        open_period=60,
    )


@router.poll_answer()
async def guess_again(
    poll: types.PollAnswer,
    state: FSMContext,
):
    state_data = await state.get_data()
    if state_data.get('correct_option_id') == poll.option_ids[0]:
        await state.update_data(
            wins_count=state_data.get('wins_count') + 1,
        )
    else:
        await state.update_data(
            lose_count=state_data.get('lose_count') + 1,
        )

    await guess(state=state, chat_id=state_data.get('chat_id'))


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
        text=(
            f'Wins: {wins_count} | Loses: {lose_count}'
            f'\nAccuracy: {accuracy:.1%}'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Try again',
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
