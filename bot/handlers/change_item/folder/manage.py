from typing import Callable
from aiogram import (
    types,
    Router,
)
from aiogram.fsm.context import FSMContext

from bot.handlers.utils.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.change_item.folder.states import ChangeFolderStates
from .callbacks import (
    ChangeFolderCallback,
    ChangeFolderNameCallback,
    DeleteFolderCallback,
    MoveFolderCallback,
)


router = Router()


@router.callback_query(ChangeFolderCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, is_root_returnable=False)
    await state.set_state(ChangeFolderStates.manage_choose_place)


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
    await state.set_state(ChangeFolderStates.manage_choose_option)
