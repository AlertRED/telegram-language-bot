from typing import Callable
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
async def choose_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse_folder.browse(callback, state)
    await state.set_state(CreateFolderStates.choose_place)


async def write_folder_name(
    foo: Callable,
    state: FSMContext,
) -> None:
    await foo(text=_('Write folder name'))
    await state.set_state(CreateFolderStates.choose_name)


@dp.callback_query(
    FolderSelectCallback.filter(),
    CreateFolderStates.choose_place,
)
async def write_folder_name_callback(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await write_folder_name(callback.message.edit_text, state)


@dp.message(CreateFolderStates.choose_name)
async def create_collection(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(new_folder_name=message.text)
    state_data = await state.get_data()

    folder = dao.get_folder(
        folder_name=state_data.get('new_folder_name'),
        parent_folder_id=state_data.get('folder_id'),
    )
    if folder:
        await message.answer(
            text=_(
                'The folder <b><u>{folder_name}</u></b>'
                ' is already exists in the folder {parent_folder_name}!'
            ).format(
                folder_name=state_data.get('new_folder_name'),
                parent_folder_name=state_data.get(
                    'parent_folder_name',
                    _('Root'),
                ),
            ),
        )
        await write_folder_name(message.answer, state)
        return

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
            folder_name=state_data.get('folder_name', _('Root')),
        ),
    )
    await state_safe_clear(state)
