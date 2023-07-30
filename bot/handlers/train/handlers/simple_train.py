from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.utils.browse_collection import start_browse
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.train.callbacks import (
    IKnowTermCallback,
    RemindTermCallback,
    SimpleTrainCallback,
)


class SimpleTrainStates(StatesGroup):
    choose_collection = State()
    show_term = State()
    remind_term = State()


@dp.callback_query(SimpleTrainCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(SimpleTrainStates.choose_collection)


@dp.callback_query(
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
        terms=[list(term) for term in terms],
        term_index=0,
    )
    await show_term(
        callback.message,
        state,
    )
    await state.set_state(SimpleTrainStates.show_term)


@dp.callback_query(IKnowTermCallback.filter())
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
            text=_(
                'Finished!'
            ),
        )


@dp.callback_query(RemindTermCallback.filter())
async def know_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    term_index = state_data['term_index']
    terms = state_data['terms']
    await callback.message.edit_text(
        text=_(
            '<u><b>{name}</b></u> - {description}'
        ).format(
            name=terms[term_index][1],
            description=terms[term_index][2],
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Ok'),
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
        text=_('{name}').format(
            name=terms[term_index][1],
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Remind me'),
                        callback_data=RemindTermCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('I know'),
                        callback_data=IKnowTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )
