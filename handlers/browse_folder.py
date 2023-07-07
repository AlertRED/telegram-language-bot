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


class FolderSelectCallback(CallbackData, prefix='bf_select_folder'):
    folder_id: Optional[int]
    folder_name: Optional[str]


class FolderChangeCallback(CallbackData, prefix='bf_change_folder'):
    folder_id: Optional[int]
    page: Optional[int] = 0


def __get_keyboard_folders_and_collections(
    telegram_user_id: int,
    folder_id: int = None,
    page: int = 0,
) -> Tuple[List[types.InlineKeyboardButton], int]:

    MAX_PERPAGE = 2
    names = []
    rows = []

    current_folder = utils.get_folder(
        telegram_user_id=telegram_user_id,
        folder_id=folder_id,
    )

    folders_count = utils.get_folders_count(
        telegram_user_id,
        folder_id=folder_id,
    )

    last_page = math.ceil(folders_count / MAX_PERPAGE)
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
                FolderChangeCallback(
                    folder_id=folder.id,
                ).pack(),
            ),
        )

    if folder_id:
        folder = utils.get_folder(telegram_user_id, folder_id)
        rows = [
            [
                types.InlineKeyboardButton(
                    text='...',
                    callback_data=FolderChangeCallback(
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
                callback_data=FolderChangeCallback(
                    folder_id=folder_id,
                    page=max(0, page - 1),
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text='>',
                callback_data=FolderChangeCallback(
                    folder_id=folder_id,
                    page=page if is_last_page else page + 1,
                ).pack(),
            ),
        ],
    )

    rows.append(
        [
            types.InlineKeyboardButton(
                text='Choose current',
                callback_data=FolderSelectCallback(
                    folder_id=current_folder.id if current_folder else None,
                    folder_name=(
                        current_folder.name if current_folder else None
                    ),
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


@router.callback_query(FolderChangeCallback.filter())
async def folder_change(
    callback: types.CallbackQuery,
    callback_data: FolderChangeCallback,
) -> None:
    await start_browse(callback, callback_data.folder_id, callback_data.page)
