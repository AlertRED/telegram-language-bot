import math
from typing import (
    List,
    Tuple,
)
from aiogram import (
    Router,
    types,
)

from .calbacks import (
    ChangeCollectionCallback,
    FolderChangeCallback,
    FolderSelectCallback,
    TermSelectedCallback,
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
    collection_id: int,
    page: int = 0,
) -> None:
    TERMS_PER_PAGE = 10
    terms = dao.get_terms(
        callback.from_user.id,
        collection_id=collection_id,
        limit=TERMS_PER_PAGE,
        offset=page * TERMS_PER_PAGE,
    )
    terms_count = dao.get_terms_count(collection_id)
    total_pages = math.ceil(terms_count / TERMS_PER_PAGE)

    text = ''
    for i, term in enumerate(terms):
        text += (
            f'\n\n{i+1}. <u><b>{term.name}</b></u> - '
            f'{term.description}'
        )

    await callback.message.edit_text(
        text=text,
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=str(i + 1),
                        callback_data=TermSelectedCallback(
                            term_id=term.id,
                        ).pack(),
                    ) for i, term in enumerate(terms)
                ],
                [
                    types.InlineKeyboardButton(
                        text='<',
                        callback_data=ChangeCollectionCallback(
                            collection_id=collection_id,
                            page=max(page - 1, 0),
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='>',
                        callback_data=ChangeCollectionCallback(
                            collection_id=collection_id,
                            page=min(page + 1, total_pages),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(ChangeCollectionCallback.filter())
async def change_page(
    callback: types.CallbackQuery,
    callback_data: ChangeCollectionCallback,
) -> None:
    await start_browse(
        callback,
        callback_data.collection_id,
        callback_data.page,
    )
