
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from bot.handlers.utils.calbacks import TermSelectedCallback
from ..states import ChangeTermStates
from ..callbacks import ChangeTermDefinitionCallback


router = Router()


@router.callback_query(ChangeTermDefinitionCallback.filter())
async def ask_new_definition(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Write new definition'
            f'(old definition is {state_data["term_description"]}):'
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_definition)


@router.message(ChangeTermStates.change_definition)
async def change_term_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    dao.update_term(
        state_data.get('term_id'),
        term_description=message.text.capitalize(),
    )
    await manage_collection(
        additional_text='Term was changed successfully!',
        send_message_foo=message.answer,
        state=state,
    )
