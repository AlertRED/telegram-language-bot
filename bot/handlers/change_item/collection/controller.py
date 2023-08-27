from typing import Callable
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.handlers.utils.handlers import browse_folder
from .states import ChangeCollectionStates
from .callbacks import (
    ChangeCollectionNameCallback,
    DeleteCollectionCallback,
    MoveCollectionCallback,
)
from ..term.callbacks import ChangeTermCallback


async def manage_collection(
    send_message_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    state_data = await state.get_data()
    await send_message_foo(
        text=_(
            '{additional_text}\n\n'
            'Manage set <u><b>{collection_name}</b></u>'
        ).format(
            additional_text=additional_text,
            collection_name=state_data.get('collection_name'),
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Change name'),
                        callback_data=ChangeCollectionNameCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Move set'),
                        callback_data=MoveCollectionCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Delete set'),
                        callback_data=DeleteCollectionCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Change term'),
                        callback_data=ChangeTermCallback(
                            collection_id=state_data.get('collection_id'),
                            collection_name=state_data.get('collection_name'),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.manage_choose_option)


async def choose_folder(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await browse_folder.browse(callback, state)
    await state.set_state(ChangeCollectionStates.choose_folder_for_moving)


async def write_collection_name(
    foo: Callable,
    state: FSMContext,
):
    state_data = await state.get_data()
    await foo(
        text=_(
            'Write new name (old name {collection_name}):'
        ).format(collection_name=state_data.get('collection_name')),
        parse_mode='html',
    )
    await state.set_state(ChangeCollectionStates.option_change_name)
