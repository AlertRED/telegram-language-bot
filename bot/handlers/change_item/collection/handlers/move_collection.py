from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.handlers.utils.browse_folder import (
    start_browse as start_browse_folder,
)
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.instances import dispatcher as dp
from .manage import manage_collection
from ..states import ChangeCollectionStates
from ..callbacks import MoveCollectionCallback


@dp.callback_query(
    MoveCollectionCallback.filter(F.sure == True),
)
async def move_collection_true(
    callback: types.CallbackQuery,
    callback_data: MoveCollectionCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        folder_id=callback_data.folder_id,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=_(
            '{collection_name} was moved to '
            '{folder_name}'
        ).format(
            collection_name=state_data["collection_name"],
            folder_name=callback_data.folder_name,
        ),
    )


@dp.callback_query(
    MoveCollectionCallback.filter(F.sure == False),
)
async def move_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@dp.callback_query(MoveCollectionCallback.filter())
async def move_collection_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse_folder(callback)
    await state.set_state(ChangeCollectionStates.choose_folder_for_moving)


@dp.callback_query(
    FolderSelectCallback.filter(),
    ChangeCollectionStates.choose_folder_for_moving,
)
async def move_collection_sure(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Are you sure wanna move '
            '<u><b>{collection_name}</b></u>'
            ' into <u><b>{folder_name}</b></u>?'
        ).format(
            collection_name=state_data["collection_name"],
            folder_name=callback_data.folder_name or "Root",
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=MoveCollectionCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=MoveCollectionCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.agree_moving)
