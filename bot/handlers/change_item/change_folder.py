from typing import Callable
import database.dao as dao
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

from bot.handlers.utils.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.change_item.callbacks import (
    ChangeFolderCallback,
    ChangeFolderNameCallback,
    DeleteFolderCallback,
    MoveFolderCallback,
)


router = Router()


class MoveFolderStates(StatesGroup):
    choose_folder = State()
    agree = State()


class ChangeFolderStates(StatesGroup):
    choose_place = State()
    change_name = State()


@router.callback_query(ChangeFolderCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, is_root_returnable=False)
    await state.set_state(ChangeFolderStates.choose_place)


@router.callback_query(
    FolderSelectCallback.filter(),
    ChangeFolderStates.choose_place,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await manage_folder(
        callback.message.edit_text,
        state,
    )


async def manage_folder(
    send_message_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    state_data = await state.get_data()
    await send_message_foo(
        text=(
            f'{additional_text}'
            f'Manage folder <u><b>{state_data["folder_name"]}</b></u>'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Change name',
                        callback_data=ChangeFolderNameCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Move folder',
                        callback_data=MoveFolderCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Delete folder',
                        callback_data=DeleteFolderCallback().pack(),
                    ),
                ],
            ],
        ),
    )


# Move folder

@router.callback_query(
    MoveFolderCallback.filter(F.sure == True),
)
async def move_folder_true(
    callback: types.CallbackQuery,
    callback_data: MoveFolderCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_folder(
        folder_id=state_data['folder_id'],
        parent_folder_id=callback_data.folder_id,
    )
    await manage_folder(
        callback.message.edit_text,
        state,
        additional_text=(
            f'{state_data["folder_name"]} was moved to '
            f'{callback_data.folder_name}\n\n'
        ),
    )


@router.callback_query(
    MoveFolderCallback.filter(F.sure == False),
)
async def move_folder_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_folder(
        callback.message.edit_text,
        state,
    )


@router.callback_query(MoveFolderCallback.filter())
async def move_folder_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse(callback)
    await state.set_state(MoveFolderStates.choose_folder)


@router.callback_query(
    FolderSelectCallback.filter(),
    MoveFolderStates.choose_folder,
)
async def move_folder_sure(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure wanna move '
            f'<u><b>{state_data["folder_name"]}</b></u>'
            f' into <u><b>{callback_data.folder_name or "Root"}</b></u>?'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=MoveFolderCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=MoveFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )


# Delete folder


@router.callback_query(DeleteFolderCallback.filter(F.sure == False))
async def delete_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_folder(
        callback.message.edit_text,
        state,
    )


@router.callback_query(DeleteFolderCallback.filter(F.sure == True))
async def delete_folder_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_folder(state_data['folder_id'])
    await callback.message.answer(
        text=(
            f'Folder <u><b>{state_data["folder_name"]}</b></u>'
            f' deleted succesfully!\n\n'
        ),
        parse_mode='html',
    )


@router.callback_query(DeleteFolderCallback.filter())
async def delete_folder_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure you wanna delete '
            f'<u><b>{state_data["folder_name"]}</b></u>?\n'
            f'All sets inside will be deleted too!'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=DeleteFolderCallback(sure=True).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=DeleteFolderCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.change_name)


# Change name

@router.callback_query(ChangeFolderNameCallback.filter())
async def change_folder_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=f'Write new name (old name {state_data["folder_name"]}):',
        parse_mode='html',
    )
    await state.set_state(ChangeFolderStates.change_name)


@router.message(
    ChangeFolderStates.change_name,
)
async def change_folder_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_folder(
        folder_id=state_data['folder_id'],
        folder_name=message.text,
    )
    await state.update_data(
        folder_name=message.text,
    )
    await manage_folder(
        message.answer,
        state,
        additional_text=(
            f'Folder name <u><b>{state_data["folder_name"]}</b></u> '
            f'changed to <u><b>{message.text}</b></u>\n\n'
        ),
    )
