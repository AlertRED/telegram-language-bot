import database.dao as dao
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from aiogram.filters.callback_data import CallbackData

from bot.handlers.browse_collection import (
    CollectionSelectCallback,
    start_browse,
)
from bot.handlers.train import SimpleTrainCallback


router = Router()


class FinishGameCallback(CallbackData, prefix='finish_find_definition'):
    win_count: int
    lose_count: int


class RemindTermCallback(CallbackData, prefix='remind_term'):
    pass


class IKnowTermCallback(CallbackData, prefix='i_know_term'):
    pass


class SimpleTrainStates(StatesGroup):
    choose_collection = State()
    show_term = State()
    remind_term = State()


@router.callback_query(SimpleTrainCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(SimpleTrainStates.choose_collection)


@router.callback_query(
    CollectionSelectCallback.filter(),
    SimpleTrainStates.choose_collection,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    terms = dao.get_simple_train_terms(callback_data.collection_id)
    await state.update_data(
        terms=terms,
        term_index=0,
    )
    await show_term(
        callback.message,
        state,
    )
    await state.set_state(SimpleTrainStates.show_term)


@router.callback_query(IKnowTermCallback.filter())
async def know_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    if state_data['term_index'] + 1 < len(state_data['terms']):
        await state.update_data(term_index=state_data['term_index'] + 1)
        await show_term(
            callback.message,
            state,
        )
    else:
        await callback.message.edit_text(
            text=(
                'Finished!'
            ),
        )


@router.callback_query(RemindTermCallback.filter())
async def know_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    term_index = state_data['term_index']
    terms = state_data['terms']
    await callback.message.edit_text(
        text=(
            f'<u><b>{terms[term_index].name}</b></u>'
            f'- {terms[term_index].description}'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Ok',
                        callback_data=IKnowTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )


async def show_term(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    term_index = state_data['term_index']
    terms = state_data['terms']

    await message.edit_text(
        text=f'{terms[term_index].name}',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Remind me',
                        callback_data=RemindTermCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='I know',
                        callback_data=IKnowTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )
