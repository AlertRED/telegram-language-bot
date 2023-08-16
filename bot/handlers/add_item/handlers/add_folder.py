from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from bot.handlers.utils.handlers import browse_folder
from bot.handlers.utils.calbacks import FolderSelectCallback
from .menu import AddingFolderCallback
from ..states import CreateFolderStates


@dp.callback_query(AddingFolderCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse_folder.browse(callback)
    await state.set_state(CreateFolderStates.choose_place)


@dp.callback_query(
    FolderSelectCallback.filter(),
    CreateFolderStates.choose_place,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await callback.message.edit_text(text=_('Write folder name'))
    await state.set_state(CreateFolderStates.choose_name)


@dp.message(CreateFolderStates.choose_name)
async def create_collection(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(new_folder_name=message.text)
    state_data = await state.get_data()
    dao.create_folder(
        telegram_user_id=message.from_user.id,
        folder_name=state_data.get('new_folder_name'),
        folder_id=state_data.get('folder_id'),
    )
    await message.answer(
        text=_(
            'Folder <b><u>{new_folder_name}</u></b> '
            'added into folder <b><u>{folder_name}</u></b>'
        ).format(
            new_folder_name=state_data.get('new_folder_name'),
            folder_name=state_data.get('folder_name'),
        ),
    )
    await state_safe_clear(state)
