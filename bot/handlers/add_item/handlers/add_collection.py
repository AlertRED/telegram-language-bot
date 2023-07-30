from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.handlers.utils.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.add_item.callbacks import AddingCollectionCallback
from bot.instances import dispatcher as dp


class CreateCollectionStates(StatesGroup):
    choose_place = State()
    choose_name = State()


@dp.callback_query(AddingCollectionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(CreateCollectionStates.choose_place)


@dp.callback_query(
    FolderSelectCallback.filter(),
    CreateCollectionStates.choose_place,
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
    await callback.message.edit_text(text=_('Write set name'))
    await state.set_state(CreateCollectionStates.choose_name)


@dp.message(CreateCollectionStates.choose_name)
async def create_collection(message: types.Message, state: FSMContext):
    await state.update_data(collection_name=message.text)
    user_data = await state.get_data()
    dao.create_collection(
        telegram_user_id=message.from_user.id,
        collection_name=user_data['collection_name'],
        folder_id=user_data['folder_id'],
    )
    await message.answer(
        text=_(
            'Set <b><u>{collection_name}</u></b> '
            'added into <b><u>{folder_name}</u></b>'
            ' folder'
        ).format(
            collection_name=user_data["collection_name"],
            folder_name=user_data["folder_name"] or "Root"
        ),
        parse_mode='html',
    )
    await state.clear()
