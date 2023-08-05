from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.utils.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.add_item.handlers.menu import AddingFolderCallback
from bot.handlers.add_item.states import CreateFolderStates


@dp.callback_query(AddingFolderCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
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
async def create_collection(message: types.Message, state: FSMContext):
    await state.update_data(new_folder_name=message.text)
    user_data = await state.get_data()
    dao.create_folder(
        telegram_user_id=message.from_user.id,
        folder_name=user_data['new_folder_name'],
        folder_id=user_data['folder_id'],
    )
    await message.answer(
        text=_(
            'Folder <b><u>{new_folder_name}</u></b> '
            'added into folder <b><u>{folder_name}</u></b>'
        ).format(
            new_folder_name=user_data["new_folder_name"],
            folder_name=user_data["folder_name"],
        ),
        parse_mode='html',
    )
    await state.clear()
