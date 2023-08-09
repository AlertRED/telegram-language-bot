from typing import Callable
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.utils.handlers.browse_folder import start_browse
from bot.handlers.utils.calbacks import FolderSelectCallback
from bot.handlers.change_item.folder.states import ChangeFolderStates
from ..callbacks import (
    ChangeFolderCallback,
    ChangeFolderNameCallback,
    DeleteFolderCallback,
    MoveFolderCallback,
)


@dp.callback_query(ChangeFolderCallback.filter())
async def choose_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, is_root_returnable=False)
    await state.set_state(ChangeFolderStates.manage_choose_place)


@dp.callback_query(
    FolderSelectCallback.filter(),
    ChangeFolderStates.manage_choose_place,
)
async def folder_choosen(
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
        text=_(
            '{additional_text}'
            'Manage folder <u><b>{folder_name}</b></u>'
        ).format(
            additional_text=additional_text,
            folder_name=state_data["folder_name"],
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Change name'),
                        callback_data=ChangeFolderNameCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Move folder'),
                        callback_data=MoveFolderCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Delete folder'),
                        callback_data=DeleteFolderCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeFolderStates.manage_choose_option)
