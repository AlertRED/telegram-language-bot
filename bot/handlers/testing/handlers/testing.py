from typing import Callable, List
from aiogram import (
    filters,
    types,
    F,
)
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

import config
import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.testing import callbacks, states
from database.models import Collection, Folder


@dp.message(
    filters.Command('testing'),
    F.from_user.id == config.MY_TELEGRAM_ID,
)
async def load_test_data(
    message: types.Message,
    state: FSMContext,
) -> None:
    await message.answer(
        text=_('Tools'),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Load test data'),
                        callback_data=(
                            callbacks.ChooseUserLoadDataCallback().pack()
                        )
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Show structure'),
                        callback_data=(
                            callbacks.ChooseUserShowStructureCallback().pack()
                        )
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Task'),
                        callback_data=callbacks.TaskCallback().pack()
                    ),
                ],
            ],
        ),
    )
    await state.set_state(states.TestingStates.choose_tool)


@dp.callback_query(callbacks.ChooseUserShowStructureCallback.filter())
async def choose_user(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(
        text=_('Choose user'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('My'),
                        callback_data=callbacks.ShowStructureCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Other'),
                        callback_data=(
                            callbacks
                            .ChooseOtherUserShowStructureCallback().pack()
                        ),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(states.TestingStates.show_structure_choose_user)


@dp.callback_query(callbacks.ChooseOtherUserShowStructureCallback.filter())
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
        text=_(
            '{additional_text}\n\nWrite user id'
        ).format(
            additional_text=additional_text,
        ),
    )
    await state.set_state(states.TestingStates.show_structure_write_user_id)


@dp.message(states.TestingStates.show_structure_write_user_id)
async def show_other_user_structure(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.text.isdigit():
        await show_structure(message.answer, int(message.text))
        await state.clear()
    else:
        await write_other_user(
            message.answer, state, _('User id must be digit!'),
        )


@dp.callback_query(callbacks.ShowStructureCallback.filter())
async def show_my_structure(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await show_structure(
        callback.message.edit_text,
        callback.from_user.id,
    )
    await state.clear()


@dp.callback_query(callbacks.ChooseOtherUserShowStructureCallback.filter())
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
        text=_(
            '{additional_text}\n\nWrite user id'
        ).format(
            additional_text=additional_text,
        ),
    )
    await state.set_state(states.TestingStates.show_structure_write_user_id)


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


@dp.callback_query(callbacks.ChooseUserLoadDataCallback.filter())
async def choose_user(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(
        text=_('Choose user'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('My'),
                        callback_data=callbacks.LoadDataCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Another'),
                        callback_data=(
                            callbacks.ChooseOtherUserLoadDataCallback().pack()
                        ),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(states.TestingStates.test_data_choose_user)


@dp.callback_query(callbacks.ChooseOtherUserLoadDataCallback.filter())
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
        text=_(
            '{additional_text}\n\nWrite user id'
        ).format(
            additional_text=additional_text,
        ),
    )
    await state.set_state(states.TestingStates.test_data_write_user_id)


@dp.message(states.TestingStates.test_data_write_user_id)
async def show_other_user_structure(
    message: types.Message,
    state: FSMContext,
) -> None:
    if message.text.isdigit():
        await load_test_data(message.answer, int(message.text))
        await state.clear()
    else:
        await write_other_user_ld(
            message.answer, state, _('User id must be digit!'),
        )


@dp.callback_query(callbacks.LoadDataCallback.filter())
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
        for g in range(1, 3):
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
        for g in range(1, 3):
            dao.create_term(
                user_id,
                collection.id,
                f'Term {i}',
                f'Definition {i}',
            )
            i += 1

    await answer_foo(
        text=_('Data added to user #{user_id}').format(user_id=user_id),
    )
