from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.constants import MAX_TERM_DEFINITION_LENGTH
from bot.misc.support import state_safe_clear
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..controller import write_new_definition
from ..callbacks import ChangeTermDefinitionCallback


router = Router()


@router.callback_query(ChangeTermDefinitionCallback.filter())
async def write_new_definition_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_new_definition(callback.message, state)


@router.message(ChangeTermStates.change_definition)
async def change_term_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    if len(message.text) > MAX_TERM_DEFINITION_LENGTH:
        await message.answer(
            text='The definition length should not be more than {max_length}!'
            .format(max_length=MAX_TERM_DEFINITION_LENGTH)
        )
        await write_new_definition(message.answer, state)
        return

    dao.update_term(
        state_data.get('term_id'),
        term_description=message.text.capitalize(),
    )
    await manage_collection(
        additional_text=_('Term was changed successfully!'),
        send_message_foo=message.answer,
        state=state,
    )
    await state_safe_clear(state)
