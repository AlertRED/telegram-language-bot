from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from database import dao
from bot.handlers.utils.handlers.browse_folder import browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from ..callbacks import ChangeFolderCallback
from ..controller import manage_folder
from ..states import ChangeFolderStates


router = Router()


@router.callback_query(ChangeFolderCallback.filter())
async def choose_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse(callback, state, is_root_returnable=False)
    await state.set_state(ChangeFolderStates.manage_choose_place)


@router.callback_query(
    FolderSelectCallback.filter(),
    ChangeFolderStates.manage_choose_place,
)
async def folder_choosen(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await manage_folder(
        callback.message.edit_text,
        state,
    )


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
