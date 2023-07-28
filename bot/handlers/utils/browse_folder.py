import math
from typing import (
    List,
    Tuple,
)
from aiogram import (
    Router,
    types,
)

from bot.handlers.utils.calbacks import (
    FolderChangeCallback,
    FolderSelectCallback,
)
import database.dao as dao


router = Router()


def __get_keyboard_folders_and_collections(
    telegram_user_id: int,
    folder_id: int = None,
    page: int = 0,
    is_root_returnable: bool = True,
) -> Tuple[List[types.InlineKeyboardButton], int]:

    MAX_PER_PAGE = 8
    names = []
    rows = []

    current_folder = dao.get_folder(
        folder_id=folder_id,
    )

    folders_count = dao.get_folders_count(
        telegram_user_id,
        folder_id=folder_id,
    )

    last_page = math.ceil(folders_count / MAX_PER_PAGE)
    is_last_page = last_page <= page + 1

    folders = dao.get_folders(
        telegram_user_id,
        folder_id,
        offset=page * MAX_PER_PAGE,
        limit=MAX_PER_PAGE,
    )
    for folder in folders:
        names.append(
            (
                '🗂' + folder.name,
                FolderChangeCallback(
                    folder_id=folder.id,
                    is_root_returnable=is_root_returnable,
                ).pack(),
            ),
        )

    if folder_id:
        folder = dao.get_folder(folder_id)
        rows = [
            [
                types.InlineKeyboardButton(
                    text='...',
                    callback_data=FolderChangeCallback(
                        folder_id=folder.parent_folder_id,
                        is_root_returnable=is_root_returnable,
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
                    is_root_returnable=is_root_returnable,
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text='>',
                callback_data=FolderChangeCallback(
                    folder_id=folder_id,
                    page=page if is_last_page else page + 1,
                    is_root_returnable=is_root_returnable,
                ).pack(),
            ),
        ],
    )
    if is_root_returnable or current_folder:
        rows.append(
            [
                types.InlineKeyboardButton(
                    text='Choose current',
                    callback_data=FolderSelectCallback(
                        folder_id=(
                            current_folder.id
                            if current_folder
                            else None
                        ),
                        folder_name=(
                            current_folder.name if current_folder else None
                        ),
                    ).pack(),
                ),
            ],
        )

    return (
        rows,
        last_page or 1,
        current_folder.name if current_folder else 'Root',
    )


async def start_browse(
    callback: types.CallbackQuery,
    folder_id: int = None,
    page: int = 0,
    is_root_returnable: bool = True,
) -> None:
    rows, last_page, root_name = __get_keyboard_folders_and_collections(
        callback.from_user.id,
        folder_id,
        page,
        is_root_returnable,
    )
    await callback.message.edit_text(
        text=(
            f'Choose folder\n'
            f'<u><b>{root_name}</b></u> page [{page + 1}/{last_page}]'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )


@router.callback_query(FolderChangeCallback.filter())
async def folder_change(
    callback: types.CallbackQuery,
    callback_data: FolderChangeCallback,
) -> None:
    await start_browse(
        callback,
        callback_data.folder_id,
        callback_data.page,
        callback_data.is_root_returnable,
    )
