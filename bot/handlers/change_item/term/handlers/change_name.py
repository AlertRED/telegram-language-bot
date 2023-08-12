
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
import database.dao as dao
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import ChangeTermNameCallback


@dp.callback_query(ChangeTermNameCallback.filter())
async def write_term_name_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_term_name(callback, state)


async def write_term_name(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await message.edit_text(
        text=_(
            'Write new name (old name is {term_name}):'
        ).format(
            term_name=state_data["term_name"],
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_name)


@dp.message(ChangeTermStates.change_name)
async def change_term_name(
    message: types.Message,
    state: FSMContext,
) -> None:
    MAX_TERM_NAME_LENGTH = 128

    await state.update_data(new_term_name=message.text.capitalize())
    state_data = await state.get_data()

    if len(state_data['new_term_name']) > MAX_TERM_NAME_LENGTH:
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
        term_name=state_data['new_term_name'],
        collection_id=state_data['collection_id'],
    )
    if term:
        await message.answer(
            text=(
                'The term <b><u>{term_name}</u></b> is already exists'
                ' in the collection {collection_name}!'
            ).format(
                term_name=state_data['new_term_name'],
                collection_name=state_data['collection_name'],
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
