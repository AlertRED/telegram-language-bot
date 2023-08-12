from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import ChangeTermDefinitionCallback


@dp.callback_query(ChangeTermDefinitionCallback.filter())
async def write_new_definition_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_new_definition(callback.message, state)


async def write_new_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await message.edit_text(
        text=_(
            'Write new definition'
            '(old definition is {term_description}):'
        ).format(
            term_description=state_data["term_description"],
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_definition)


@dp.message(ChangeTermStates.change_definition)
async def change_term_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    MAX_TERM_DEFINITION_LENGTH = 256

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
