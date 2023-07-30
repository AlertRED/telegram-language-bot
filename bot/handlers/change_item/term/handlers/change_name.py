
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
from ..callbacks import ChangeTermNameCallback


@dp.callback_query(ChangeTermNameCallback.filter())
async def change_term(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await callback.message.edit_text(
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
    state_data = await state.get_data()
    dao.update_term(
        state_data.get('term_id'),
        term_name=message.text.capitalize(),
    )
    await manage_collection(
        additional_text=_('Term was changed successfully!'),
        send_message_foo=message.answer,
        state=state,
    )
