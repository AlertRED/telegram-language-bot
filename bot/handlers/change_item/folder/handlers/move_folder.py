from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
import database.dao as dao
from bot.handlers.utils.handlers.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from .manage import manage_folder
from ..states import ChangeFolderStates
from ..callbacks import MoveFolderCallback


@dp.callback_query(
    MoveFolderCallback.filter(F.sure == True),
)
async def move_folder_true(
    callback: types.CallbackQuery,
    callback_data: MoveFolderCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_folder(
        folder_id=state_data['folder_id'],
        parent_folder_id=callback_data.folder_id,
    )
    await manage_folder(
        callback.message.edit_text,
        state,
        additional_text=_(
            '{folder_name} was moved to '
            '{selected_folder_name}\n\n'
        ).format(
            folder_name=state_data["folder_name"],
            selected_folder_name=callback_data.folder_name,
        ),
    )


@dp.callback_query(
    MoveFolderCallback.filter(F.sure == False),
)
async def move_folder_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_folder(
        callback.message.edit_text,
        state,
    )


@dp.callback_query(MoveFolderCallback.filter())
async def move_folder_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await start_browse(callback, exclude_folders_ids=[state_data['folder_id']])
    await state.set_state(ChangeFolderStates.choose_folder_for_moving)


@dp.callback_query(
    FolderSelectCallback.filter(),
    ChangeFolderStates.choose_folder_for_moving,
)
async def move_folder_sure(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Are you sure wanna move '
            '<u><b>{folder_name}</b></u>'
            ' into <u><b>{selected_folder_name}</b></u>?'
        ).format(
            folder_name=state_data["folder_name"],
            selected_folder_name=callback_data.folder_name or "Root",
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=MoveFolderCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=MoveFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.agree_moving)
