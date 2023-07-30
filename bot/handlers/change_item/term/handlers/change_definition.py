
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
import database.dao as dao
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from bot.handlers.utils.calbacks import TermSelectedCallback
from ..states import ChangeTermStates
from ..callbacks import ChangeTermDefinitionCallback


@dp.callback_query(ChangeTermDefinitionCallback.filter())
async def ask_new_definition(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await callback.message.edit_text(
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
    state_data = await state.get_data()
    dao.update_term(
        state_data.get('term_id'),
        term_description=message.text.capitalize(),
    )
    await manage_collection(
        additional_text=_('Term was changed successfully!'),
        send_message_foo=message.answer,
        state=state,
    )
