from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from bot.handlers.utils.handlers.browse_folder import browse
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
        folder_id=state_data.get('folder_id'),
        parent_folder_id=callback_data.folder_id,
    )
    await manage_folder(
        callback.message.edit_text,
        state,
        additional_text=_(
            '{folder_name} was moved to '
            '{selected_folder_name}\n\n'
        ).format(
            folder_name=state_data.get('folder_name'),
            selected_folder_name=callback_data.folder_name,
        ),
    )
    await state_safe_clear(state)


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
async def move_folder_browse_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await move_folder_browse(callback, state)


async def move_folder_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()

    parent_folder_id = dao.get_folder(
        folder_id=state_data.get('folder_id'),
    ).parent_folder_id
    await state.update_data(
        exclude_folders_ids=(
            [parent_folder_id]
            if parent_folder_id
            else parent_folder_id
        )
    )
    await browse(callback, state)
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
    folder = dao.get_folder(
        telegram_user_id=callback.from_user.id,
        folder_name=state_data.get('folder_name'),
    )
    folder = dao.get_folder(
        telegram_user_id=callback.from_user.id,
        folder_id=folder.parent_folder_id,
        folder_name=state_data.get('folder_new_name'),
    )
    if folder:
        await callback.message.answer(
            text=(
                'The folder <b><u>{folder_name}</u></b> is already'
                ' exists in this folder!'
            ).format(
                folder_name=state_data.get('folder_new_name'),
            ),
        )
        await move_folder_browse(callback, state)
        return

    await callback.message.edit_text(
        text=_(
            'Are you sure wanna move '
            '<u><b>{folder_name}</b></u>'
            ' into <u><b>{selected_folder_name}</b></u>?'
        ).format(
            folder_name=state_data.get('folder_name'),
            selected_folder_name=callback_data.folder_name or 'Root',
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
