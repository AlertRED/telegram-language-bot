from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from .manage import manage_folder
from .states import ChangeFolderStates
from .callbacks import DeleteFolderCallback


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
    dao.delete_folder(state_data['folder_id'])
    await callback.message.answer(
        text=(
            f'Folder <u><b>{state_data["folder_name"]}</b></u>'
            f' deleted succesfully!\n\n'
        ),
        parse_mode='html',
    )


@router.callback_query(DeleteFolderCallback.filter())
async def delete_folder_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure you wanna delete '
            f'<u><b>{state_data["folder_name"]}</b></u>?\n'
            f'All sets inside will be deleted too!'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=DeleteFolderCallback(sure=True).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=DeleteFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.agree_delete)
