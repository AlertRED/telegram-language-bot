from typing import Callable, List
from aiogram import (
    Router,
    filters,
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

import database.dao as dao
from database.models import Collection, Folder
from config import MY_TELEGRAM_ID


router = Router()


class TestingStates(StatesGroup):
    choose_tool = State()
    show_structure_choose_user = State()
    show_structure_write_user_id = State()
    test_data_choose_user = State()
    test_data_write_user_id = State()


class TaskCallback(CallbackData, prefix='task'):
    pass


class ShowStructureCallback(CallbackData, prefix='show_structure'):
    pass


class ChooseUserShowStructureCallback(
    CallbackData,
    prefix='choose_user_show_structure',
):
    pass


class ChooseOtherUserShowStructureCallback(
    CallbackData,
    prefix='choose_other_user_show_structure',
):
    pass


class LoadDataCallback(CallbackData, prefix='load_data'):
    pass


class ChooseUserLoadDataCallback(
    CallbackData,
    prefix='choose_user_load_data',
):
    pass


class ChooseOtherUserLoadDataCallback(
    CallbackData,
    prefix='choose_other_user_load_data',
):
    pass


@router.message(filters.Command('testing'), F.from_user.id == MY_TELEGRAM_ID)
async def load_test_data(
    message: types.Message,
    state: FSMContext,
) -> None:
    await message.answer(
        text='Tools',
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Load test data',
                        callback_data=ChooseUserLoadDataCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Show structure',
                        callback_data=ChooseUserShowStructureCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Task',
                        callback_data=TaskCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(TestingStates.choose_tool)


@router.callback_query(ChooseUserShowStructureCallback.filter())
async def choose_user(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(
        text='Choose user',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='My',
                        callback_data=ShowStructureCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='Other',
                        callback_data=(
                            ChooseOtherUserShowStructureCallback().pack()
                        ),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(TestingStates.show_structure_choose_user)


@router.callback_query(ChooseOtherUserShowStructureCallback.filter())
async def write_other_user_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_other_user(callback.message.edit_text, state)


async def write_other_user(
    send_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    await send_foo(
        text=f'{additional_text}Write user id',
    )
    await state.set_state(TestingStates.show_structure_write_user_id)


@router.message(TestingStates.show_structure_write_user_id)
async def show_other_user_structure(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.text.isdigit():
        await show_structure(message.answer, int(message.text))
        await state.clear()
    else:
        await write_other_user(
            message.answer, state, 'User id must be digit!\n\n',
        )


@router.callback_query(ShowStructureCallback.filter())
async def show_my_structure(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await show_structure(
        callback.message.edit_text,
        callback.from_user.id,
    )
    await state.clear()


@router.callback_query(ChooseOtherUserShowStructureCallback.filter())
async def write_other_user_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_other_user(callback.message.edit_text, state)


async def write_other_user(
    send_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    await send_foo(
        text=f'{additional_text}Write user id',
    )
    await state.set_state(TestingStates.show_structure_write_user_id)


async def show_structure(
    answer_foo: Callable,
    user_id: int,
) -> None:
    output = ''
    folders = [
        (1, folder)
        for folder in dao.get_folders(user_id, parent_folder_id=None)
    ] + [(0, None)]
    while folders:
        deep_index, folder = folders.pop()
        folder_id = folder.id if folder else None
        folder_name = folder.name if folder else 'Root'

        folders += [
            (deep_index + 1, folder)
            for folder in dao.get_folders(user_id, parent_folder_id=folder_id)
        ]

        space = deep_index * 2
        output += f'{" " * space}+-{folder_name}\n'
        for collection in dao.get_collections(user_id, folder_id):
            output += f'{" " * (space + 2)}::{collection.name}\n'
            for term in dao.get_terms(user_id, collection.id):
                output += f'{" " * (space + 2)}| {term.name}\n'

    await answer_foo(
        text=f'<code>{output}</code>',
        parse_mode='html',
    )


@router.callback_query(ChooseUserLoadDataCallback.filter())
async def choose_user(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(
        text='Choose user',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='My',
                        callback_data=LoadDataCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='Other',
                        callback_data=ChooseOtherUserLoadDataCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(TestingStates.test_data_choose_user)


@router.callback_query(ChooseOtherUserLoadDataCallback.filter())
async def write_other_user_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await write_other_user_ld(callback.message.edit_text, state)


async def write_other_user_ld(
    send_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    await send_foo(
        text=f'{additional_text}Write user id',
    )
    await state.set_state(TestingStates.test_data_write_user_id)


@router.message(TestingStates.test_data_write_user_id)
async def show_other_user_structure(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.text.isdigit():
        await load_test_data(message.answer, int(message.text))
        await state.clear()
    else:
        await write_other_user_ld(
            message.answer, state, 'User id must be digit!\n\n',
        )


@router.callback_query(LoadDataCallback.filter())
async def show_my_structure(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await load_test_data(
        callback.message.edit_text,
        callback.from_user.id,
    )
    await state.clear()


async def load_test_data(
    answer_foo: Callable,
    user_id: int,
) -> None:
    folders: List[Folder] = []
    for folder_num in range(1, 6):
        folders.append(
            dao.create_folder(
                user_id,
                f'Folder#{folder_num}',
            ),
        )

    i = 1
    collections: List[Collection] = []
    for folder in folders:
        for _ in range(1, 3):
            collections.append(
                dao.create_collection(
                    user_id,
                    f'Set#{i}',
                    folder.id,
                ),
            )
            i += 1

    i = 1
    for collection in collections:
        for _ in range(1, 3):
            dao.create_term(
                user_id,
                collection.id,
                f'term_name_{i}',
                f'term_definition_{i}',
            )
            i += 1

    await answer_foo(
        text=f'Data added to user #{user_id}',
    )
