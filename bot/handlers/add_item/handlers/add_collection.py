from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.handlers.add_item.controller import write_collection_name
from bot.misc.support import state_safe_clear
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.utils.handlers import browse_folder
from ..callbacks import AddCollectionCallback
from ..states import CreateCollectionStates


router = Router()


@router.callback_query(AddCollectionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse_folder.browse(callback, state)
    await state.set_state(CreateCollectionStates.choose_place)


@router.callback_query(
    FolderSelectCallback.filter(),
    CreateCollectionStates.choose_place,
)
async def write_collection_name_callback(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await write_collection_name(callback.message.edit_text, state)


@router.message(CreateCollectionStates.choose_name)
async def create_collection(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(collection_name=message.text)
    state_data = await state.get_data()

    collection = dao.get_collection(
        collection_name=state_data.get('collection_name'),
        folder_id=state_data.get('folder_id'),
    )
    if collection:
        await message.answer(
            text=_(
                'The collection <b><u>{collection_name}</u></b>'
                ' is already exists in the folder {folder_name}!'
            ).format(
                collection_name=state_data.get('collection_name'),
                folder_name=state_data.get('folder_name'),
            ),
        )
        await write_collection_name(message.answer, state)
        return

    dao.create_collection(
        telegram_user_id=message.from_user.id,
        collection_name=state_data.get('collection_name'),
        folder_id=state_data.get('folder_id'),
    )
    await message.answer(
        text=_(
            'Set <b><u>{collection_name}</u></b> '
            'added into <b><u>{folder_name}</u></b> folder'
        ).format(
            collection_name=state_data.get('collection_name'),
            folder_name=state_data.get('folder_name', _('Root')),
        ),
    )
    await state_safe_clear(state)
