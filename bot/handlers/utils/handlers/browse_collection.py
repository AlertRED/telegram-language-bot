import math
from typing import (
    List, Tuple,
)
from aiogram import Router, types
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

from bot.misc.constants import MAX_ITEMS_PAGE_BROWSE_COLLECTIONS
from bot.handlers.utils.calbacks import (
    CollectionSelectCallback, FolderChangedCallback,
)
import database.dao as dao


router = Router()


def __get_keyboard_folders_and_collections(
    telegram_user_id: int,
    exclude_collection_ids: list,
    folder_id: int = None,
    page: int = 0,
) -> Tuple[List[types.InlineKeyboardButton], int]:

    names = []
    rows = []

    folders_count = dao.get_folders_count(
        telegram_user_id,
        folder_id=folder_id,
    )

    collections_count = dao.get_collections_count(
        telegram_user_id,
        folder_id=folder_id,
        exclude_collection_ids=exclude_collection_ids,
    )

    last_page = math.ceil(
        (folders_count + collections_count)
        / MAX_ITEMS_PAGE_BROWSE_COLLECTIONS
    )
    is_last_page = last_page <= page + 1

    folders = dao.get_folders(
        telegram_user_id,
        folder_id,
        offset=page * MAX_ITEMS_PAGE_BROWSE_COLLECTIONS,
        limit=MAX_ITEMS_PAGE_BROWSE_COLLECTIONS,
    )
    for folder in folders:
        names.append(
            (
                '🗂' + folder.name,
                FolderChangedCallback(
                    folder_id=folder.id,
                ).pack(),
            ),
        )
    if len(folders) < MAX_ITEMS_PAGE_BROWSE_COLLECTIONS:
        offset = max(page * MAX_ITEMS_PAGE_BROWSE_COLLECTIONS - folders_count, 0)
        collections = dao.get_collections(
            telegram_user_id,
            folder_id,
            offset=offset,
            limit=MAX_ITEMS_PAGE_BROWSE_COLLECTIONS - len(folders),
            exclude_collection_ids=exclude_collection_ids,
        )
        for collection in collections:
            names.append(
                (
                    '📄' + collection.name,
                    CollectionSelectCallback(
                        collection_name=collection.name,
                        collection_id=collection.id,
                    ).pack(),
                ),
            )

    if folder_id:
        folder = dao.get_folder(folder_id)
        rows = [
            [
                types.InlineKeyboardButton(
                    text='...',
                    callback_data=FolderChangedCallback(
                        folder_id=folder.parent_folder_id,
                    ).pack(),
                ),
            ],
        ]

    for i in range(0, len(names), 2):
        rows.append(
            [
                types.InlineKeyboardButton(
                    text=name,
                    callback_data=callback,
                )
                for name, callback in names[i:i + 2]
            ],
        )
    rows.append(
        [
            types.InlineKeyboardButton(
                text='<',
                callback_data=FolderChangedCallback(
                    folder_id=folder_id,
                    page=max(0, page - 1),
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text='>',
                callback_data=FolderChangedCallback(
                    folder_id=folder_id,
                    page=page if is_last_page else page + 1,
                ).pack(),
            ),
        ],
    )

    return rows, last_page or 1


async def browse(
    callback: types.CallbackQuery,
    state: FSMContext,
    folder_id: int = None,
    page: int = 0,
) -> None:
    state_data = await state.get_data()
    exclude_collection_ids = state_data.get('exclude_collection_ids')
    if exclude_collection_ids is None:
        exclude_collection_ids = []
    rows, last_page = __get_keyboard_folders_and_collections(
        callback.from_user.id,
        exclude_collection_ids,
        folder_id,
        page,
    )
    await callback.message.edit_text(
        text=_(
            'Choose set [{current_page}/{last_page}]'
        ).format(
            current_page=page + 1,
            last_page=last_page,
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )


@router.callback_query(FolderChangedCallback.filter())
async def folder_chosen(
    callback: types.CallbackQuery,
    callback_data: FolderChangedCallback,
    state: FSMContext,
) -> None:
    await browse(
        callback,
        state,
        callback_data.folder_id,
        callback_data.page,
    )
