from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from .manage import manage_collection
from ..states import ChangeCollectionStates
from ..callbacks import DeleteCollectionCallback
import database.dao as dao


@dp.callback_query(DeleteCollectionCallback.filter(F.sure == False))
async def delete_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@dp.callback_query(DeleteCollectionCallback.filter(F.sure == True))
async def delete_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_collection(state_data.get('collection_id'))
    await callback.message.edit_text(
        text=_(
            'Collection <u><b>{collection_name}</b></u>'
            ' deleted succesfully!'
        ).format(
            collection_name=state_data.get('collection_name'),
        ),
        parse_mode='html',
    )
    await state_safe_clear(state)


@dp.callback_query(DeleteCollectionCallback.filter())
async def delete_collection_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Are you sure you wanna delete '
            '<u><b>{collection_name}</b></u>?\n'
            'All terms inside will be deleted too!'
        ).format(
            collection_name=state_data.get('collection_name'),
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=DeleteCollectionCallback(
                            sure=True,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=DeleteCollectionCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.agree_delete)
