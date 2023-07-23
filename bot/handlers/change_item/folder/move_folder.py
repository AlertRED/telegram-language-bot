from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from bot.handlers.utils.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from .manage import manage_folder
from .states import ChangeFolderStates
from .callbacks import MoveFolderCallback


router = Router()


@router.callback_query(
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
        additional_text=(
            f'{state_data["folder_name"]} was moved to '
            f'{callback_data.folder_name}\n\n'
        ),
    )


@router.callback_query(
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


@router.callback_query(MoveFolderCallback.filter())
async def move_folder_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse(callback)
    await state.set_state(ChangeFolderStates.choose_folder_for_moving)


@router.callback_query(
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
        text=(
            f'Are you sure wanna move '
            f'<u><b>{state_data["folder_name"]}</b></u>'
            f' into <u><b>{callback_data.folder_name or "Root"}</b></u>?'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=MoveFolderCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=MoveFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.agree_moving)
