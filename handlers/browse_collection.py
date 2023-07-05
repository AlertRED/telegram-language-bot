import math
from typing import (
    List,
    Optional,
    Tuple,
)
from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

import utils


router = Router()


class SelectedFolderCallback(CallbackData, prefix='selected_folder'):
    folder_id: Optional[int]
    page: Optional[int]


class SelectedCollectionCallback(CallbackData, prefix='selected_collection'):
    collection_name: str


def __get_keyboard_folders(
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
                SelectedFolderCallback(
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
                    SelectedCollectionCallback(
                        collection_name=collection.name,
                    ).pack(),
                ),
            )

    if folder_id:
        folder = utils.get_folder(telegram_user_id, folder_id)
        rows = [
            [
                types.InlineKeyboardButton(
                    text='...',
                    callback_data=SelectedFolderCallback(
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
                callback_data=SelectedFolderCallback(
                    folder_id=folder_id,
                    page=max(0, page - 1),
                ).pack(),
            ),
            types.InlineKeyboardButton(
                text='>',
                callback_data=SelectedFolderCallback(
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


async def __choose_set(
        message: types.Message,
        telegram_user_id: int,
        folder_id: int = None,
        page: int = 0,
) -> None:

    rows, last_page = __get_keyboard_folders(telegram_user_id, folder_id, page)
    await message.answer(
        text=f'Choose set [{page + 1}/{last_page}]',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )


@router.message(filters.Command('add_term'))
async def choose_set(
    message: types.Message,
    state: FSMContext,
) -> None:
    await __choose_set(
        message=message,
        telegram_user_id=message.chat.id,
        page=0,
    )


@router.callback_query(SelectedFolderCallback.filter())
async def folder_chosen(
    callback: types.CallbackQuery,
    callback_data: SelectedFolderCallback,
    state: FSMContext,
) -> None:
    await __choose_set(
        message=callback.message,
        telegram_user_id=callback.from_user.id,
        folder_id=callback_data.folder_id,
        page=callback_data.page or 0,
    )




# @router.message(
#     AddTerm.adding_term_name,
# )
# async def food_chosen(message: types.Message, state: FSMContext):
#     await state.update_data(chosen_food=message.text)
#     user_data = await state.get_data()
#     await message.answer(
#         text=f'Write description for <b><u>{user_data["chosen_food"]}</u></b>:',
#         parse_mode='html',
#     )
#     await state.set_state(AddTerm.adding_term_description)


# @router.message(AddTerm.adding_term_description)
# async def food_size_chosen(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     await message.answer(
#         text=f'Term added\n'
#         f'Term: <b><u>{user_data["chosen_food"]}</u></b>\n'
#         f'Description: {message.text}',
#         parse_mode='html',
#     )
#     await state.clear()


# @router.message(AddTerm.adding_term_description)
# async def food_size_chosen_incorrectly(message: types.Message):
#     await message.answer(
#         text='Я не знаю такого размера порции.\n\n'
#              'Пожалуйста, выберите один из вариантов из списка ниже:',
#         reply_markup=make_row_keyboard(available_food_sizes),
#     )
