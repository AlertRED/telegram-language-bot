from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.support import state_safe_clear
from .manage import manage_folder
from ..states import ChangeFolderStates
from ..callbacks import DeleteFolderCallback


router = Router()


@router.callback_query(DeleteFolderCallback.filter(F.sure == False))
async def delete_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_folder(
        callback.message.edit_text,
        state,
    )


@router.callback_query(DeleteFolderCallback.filter(F.sure == True))
async def delete_folder_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_folder(state_data.get('folder_id'))
    await callback.message.edit_text(
        text=_(
            'Folder <u><b>{folder_name}</b></u>'
            ' deleted succesfully!'
        ).format(
            folder_name=state_data.get('folder_name'),
        ),
        parse_mode='html',
    )
    await state_safe_clear(state)


@router.callback_query(DeleteFolderCallback.filter())
async def delete_folder_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Are you sure you wanna delete '
            '<u><b>{folder_name}</b></u>?\n'
            'All sets inside will be deleted too!'
        ).format(
            folder_name=state_data.get('folder_name'),
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=DeleteFolderCallback(sure=True).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=DeleteFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.agree_delete)
