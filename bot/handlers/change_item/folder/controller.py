from typing import Callable
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.handlers.change_item.folder.callbacks import (
    ChangeFolderNameCallback, DeleteFolderCallback, MoveFolderCallback,
)
from bot.handlers.change_item.folder.states import ChangeFolderStates


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
            folder_name=state_data.get('folder_name'),
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


async def write_folder_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.edit_text(
        text=_(
            'Write new name (old name {folder_name}):'
        ).format(
            folder_name=state_data.get('folder_name'),
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeFolderStates.option_change_name)
