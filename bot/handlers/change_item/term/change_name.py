
from aiogram import (
    types,
    Router,
)
from aiogram.fsm.context import FSMContext

from bot.handlers.change_item.change_collection import manage_collection
from bot.handlers.utils.calbacks import TermSelectedCallback
import database.dao as dao
from .callbacks import ChangeTermNameCallback
from . import router, ChangeTermStates


router = Router()


@router.callback_query(ChangeTermNameCallback.filter())
async def change_term(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=f'Write new name (old name {state_data["term_name"]}):',
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_name)


@router.message(ChangeTermStates.change_name)
async def change_term_name(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    dao.update_term(
        state_data.get('term_id'),
        term_name=message.text.capitalize(),
    )
    await manage_collection(
        additional_text='Term was changed successfully!',
        send_message_foo=message.answer,
        state=state,
    )
