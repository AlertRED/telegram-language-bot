from aiogram import Router
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from .manage import manage_folder
from ..states import ChangeFolderStates
from ..callbacks import ChangeFolderNameCallback


router = Router()


@router.callback_query(ChangeFolderNameCallback.filter())
async def change_folder_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=f'Write new name (old name {state_data["folder_name"]}):',
        parse_mode='html',
    )
    await state.set_state(ChangeFolderStates.option_change_name)


@router.message(
    ChangeFolderStates.option_change_name,
)
async def change_folder_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_folder(
        folder_id=state_data['folder_id'],
        folder_name=message.text,
    )
    await state.update_data(
        folder_name=message.text,
    )
    await manage_folder(
        message.answer,
        state,
        additional_text=(
            f'Folder name <u><b>{state_data["folder_name"]}</b></u> '
            f'changed to <u><b>{message.text}</b></u>\n\n'
        ),
    )
