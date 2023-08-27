from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.constants import MIN_TERMS_COUNT_FIND_DEFINITION
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.utils.handlers.browse_collection import browse
from bot.handlers.train.handlers.menu import train_menu
from bot.handlers.train.controller import (
    cancel_expired_time_job, finish_train, guess, update_score
)

from ..callbacks import (
    FindDefinitionCallback, FinishTrainCallback, NextTryCallback,
)
from ..states import FindDefinitionStates


router = Router()


@router.callback_query(FindDefinitionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse(callback, state=state, folder_id=None, page=0)
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
    terms_count = dao.get_terms_count(
        telegram_user_id=callback.from_user.id,
        collection_id=callback_data.collection_id,
    )
    if terms_count < MIN_TERMS_COUNT_FIND_DEFINITION:
        await callback.message.answer(
            text=_(
                'Sorry, set must contains more than <b>{min_terms_count}</b>'
                ' terms, set <b><u>{collection_name}</u></b> has '
                '<b>{term_counts}</b> terms'
            ).format(
                min_terms_count=MIN_TERMS_COUNT_FIND_DEFINITION,
                collection_name=callback_data.collection_name,
                term_counts=terms_count,
            ),
        )
        await train_menu(callback.message)
    else:
        await state.update_data(
            collection_id=callback_data.collection_id,
            collection_name=callback_data.collection_name,
            wins_count=0,
            lose_count=0,
            used_term_ids=[],
            chat_id=callback.message.chat.id,
        )
        if (await state.get_state()) == FindDefinitionStates.choose_collection:
            await callback.message.delete()
        await guess(state=state)
        await state.set_state(FindDefinitionStates.try_guess)


@router.callback_query(NextTryCallback.filter())
async def next_try(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await guess(state=state)


@router.poll_answer()
async def get_poll_answer(
    poll: types.PollAnswer,
    state: FSMContext,
):
    state_data = await state.get_data()
    await update_score(
        state_data.get('correct_option_id') == poll.option_ids[0],
        state,
    )
    await cancel_expired_time_job(state)
    await guess(state=state)


@router.callback_query(FinishTrainCallback.filter())
async def finish_train_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await cancel_expired_time_job(state)
    message_id = (
        None
        if callback.message.content_type is not types.ContentType.TEXT
        else callback.message.message_id
    )
    await finish_train(
        state,
        message_id=message_id,
    )
