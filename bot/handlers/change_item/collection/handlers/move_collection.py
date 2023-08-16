from aiogram import (
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.handlers.support import state_safe_clear
from bot.handlers.utils.handlers.browse_folder import (
    browse as start_browse_folder,
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
        collection_id=state_data.get('collection_id'),
        folder_id=callback_data.folder_id,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=_(
            '{collection_name} was moved to '
            '{folder_name}'
        ).format(
            collection_name=state_data.get('collection_name'),
            folder_name=callback_data.folder_name,
        ),
    )
    await state_safe_clear(state)


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
async def browse_folder_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    parent_folder_id = dao.get_collection(
        collection_id=state_data.get('collection_id'),
    ).folder_id
    await state.update_data(
        exclude_folders_ids=(
            [parent_folder_id]
            if parent_folder_id
            else parent_folder_id
        )
    )
    await brows_folder(callback, state)


async def brows_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse_folder(callback, state)
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
    collection = dao.get_collection(
        telegram_user_id=callback.from_user.id,
        collection_name=state_data.get('collection_name'),
    )
    collection = dao.get_collection(
        telegram_user_id=callback.from_user.id,
        folder_id=collection.folder_id,
        collection_name=state_data.get('collection_new_name'),
    )
    if collection:
        await callback.message.answer(
            text=(
                'The collection <b><u>{collection_name}</u></b> is already'
                ' exists in this folder!'
            ).format(
                collection_name=state_data.get('folder_new_name'),
            ),
        )
        await brows_folder(callback, state)
        return

    await callback.message.edit_text(
        text=_(
            'Are you sure wanna move '
            '<u><b>{collection_name}</b></u>'
            ' into <u><b>{folder_name}</b></u>?'
        ).format(
            collection_name=state_data.get('collection_name'),
            folder_name=callback_data.folder_name or 'Root',
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
