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


class CollectionSelectedCallback(CallbackData, prefix='select_collection'):
    collection_id: int
    collection_name: str


class FolderSelectedCallback(CallbackData, prefix='select_folder'):
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
                FolderSelectedCallback(
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
                    CollectionSelectedCallback(
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
                    callback_data=FolderSelectedCallback(
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
                callback_data=FolderSelectedCallback(
                    folder_id=folder_id,
                    page=max(0, page - 1),
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text='>',
                callback_data=FolderSelectedCallback(
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


# async def __choose_collection(
#     message: types.Message,
#     telegram_user_id: int,
#     folder_id: int = None,
#     page: int = 0,
#     is_edit_message: bool = False,
# ) -> None:
#     rows, last_page = __get_keyboard_folders_and_collections(telegram_user_id, folder_id, page)
#     if is_edit_message:
#         await message.edit_text(
#             text=f'Choose set [{page + 1}/{last_page}]',
#             reply_markup=types.InlineKeyboardMarkup(
#                 inline_keyboard=rows,
#             ),
#         )
#     else:
#         await message.answer(
#             text=f'Choose set [{page + 1}/{last_page}]',
#             reply_markup=types.InlineKeyboardMarkup(
#                 inline_keyboard=rows,
#             ),
#         )

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


@router.callback_query(FolderSelectedCallback.filter())
async def folder_chosen(
    callback: types.CallbackQuery,
    callback_data: FolderSelectedCallback,
) -> None:
    await start_browse(callback, callback_data.folder_id, callback_data.page)
    # else:
    #     await message.answer(
    #         text=f'Choose set [{page + 1}/{last_page}]',
    #         reply_markup=types.InlineKeyboardMarkup(
    #             inline_keyboard=rows,
    #         ),
    #     )


# @router.callback_query(SelectedCollectionCallback.filter())
# async def collection_chosen(
#     callback: types.CallbackQuery,
#     callback_data: SelectedCollectionCallback,
#     state: FSMContext,
# ) -> None:
#     await state.update_data(
#         collection_name=callback_data.collection_name,
#         collection_id=callback_data.collection_id,
#     )
#     data = await state.get_data()
#     foo = data.get('callback_foo')
#     await foo(callback, state)



