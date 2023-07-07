import math
from typing import (
    List,
    Optional,
    Tuple,
)
from aiogram import (
    Router,
    types,
)
from aiogram.filters.callback_data import CallbackData

import utils


router = Router()


class CollectionSelectCallback(CallbackData, prefix='select_collection'):
    collection_id: int
    collection_name: str


class FolderChangedCallback(CallbackData, prefix='change_folder'):
    folder_id: Optional[int]
    page: Optional[int] = 0


def __get_keyboard_folders_and_collections(
    telegram_user_id: int,
    folder_id: int = None,
    page: int = 0,
) -> Tuple[List[types.InlineKeyboardButton], int]:

    MAX_PERPAGE = 3
    names = []
    rows = []

    folders_count = utils.get_folders_count(
        telegram_user_id,
        folder_id=folder_id,
    )

    collections_count = utils.get_collections_count(
        telegram_user_id,
        folder_id=folder_id,
    )

    last_page = math.ceil((folders_count + collections_count) / MAX_PERPAGE)
    is_last_page = last_page <= page + 1

    folders = utils.get_folders(
        telegram_user_id,
        folder_id,
        offset=page * MAX_PERPAGE,
        limit=MAX_PERPAGE,
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
    if len(folders) < MAX_PERPAGE:
        offset = page * MAX_PERPAGE - folders_count
        collections = utils.get_collections(
            telegram_user_id,
            folder_id,
            offset=offset,
            limit=MAX_PERPAGE - len(folders),
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
        folder = utils.get_folder(telegram_user_id, folder_id)
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

    rows.append(
        [
            types.InlineKeyboardButton(
                text='Go back',
                callback_data='go_back',
            ),
        ],
    )
    return rows, last_page


async def start_browse(
    callback: types.CallbackQuery,
    folder_id: int,
    page: int,
) -> None:
    rows, last_page = __get_keyboard_folders_and_collections(
        callback.from_user.id, folder_id, page,
    )
    await callback.message.edit_text(
        text=f'Choose set [{page + 1}/{last_page}]',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )


@router.callback_query(FolderChangedCallback.filter())
async def folder_chosen(
    callback: types.CallbackQuery,
    callback_data: FolderChangedCallback,
) -> None:
    await start_browse(callback, callback_data.folder_id, callback_data.page)
