from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.constants import MAX_TERM_NAME_LENGTH
from bot.misc.support import state_safe_clear
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..controller import write_term_name
from ..states import ChangeTermStates
from ..callbacks import ChangeTermNameCallback


router = Router()


@router.callback_query(ChangeTermNameCallback.filter())
async def write_term_name_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_term_name(callback.message.edit_text, state)


@router.message(ChangeTermStates.change_name)
async def change_term_name(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(new_term_name=message.text.capitalize())
    state_data = await state.get_data()

    if len(state_data.get('new_term_name')) > MAX_TERM_NAME_LENGTH:
        await message.answer(
            text=(
                'The term length should not be more than {max_length}!'
            ).format(
                max_length=MAX_TERM_NAME_LENGTH,
            )
        )
        await write_term_name(message.answer, state)
        return

    term = dao.get_term(
        term_name=state_data.get('new_term_name'),
        collection_id=state_data.get('collection_id'),
    )
    if term:
        await message.answer(
            text=(
                'The term <b><u>{term_name}</u></b> is already exists'
                ' in the collection {collection_name}!'
            ).format(
                term_name=state_data.get('new_term_name'),
                collection_name=state_data.get('collection_name'),
            ),
        )
        await write_term_name(message.answer, state)
        return

    dao.update_term(
        state_data.get('term_id'),
        term_name=message.text.capitalize(),
    )
    await manage_collection(
        additional_text=_('Term was changed successfully!'),
        send_message_foo=message.answer,
        state=state,
    )
    await state_safe_clear(state)
