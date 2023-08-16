from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import DeleteTermCallback
import database.dao as dao


@dp.callback_query(DeleteTermCallback.filter(F.sure == False))
async def delete_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@dp.callback_query(DeleteTermCallback.filter(F.sure == True))
async def delete_term_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_term(state_data.get('term_id'))
    additional_text = _(
        'Term <u><b>{term_name}</b></u>'
        ' deleted succesfully!'
    ).format(
        term_name=state_data.get('term_name'),
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=additional_text,
    )
    await state_safe_clear(state)


@dp.callback_query(DeleteTermCallback.filter())
async def delete_term_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Are you sure you wanna delete '
            '<u><b>{term_name}</b></u>?\n'
        ).format(
            term_name=state_data.get('term_name'),
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=DeleteTermCallback(
                            sure=True,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=DeleteTermCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.agree_delete)
