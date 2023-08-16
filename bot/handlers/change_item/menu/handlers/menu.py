from aiogram import (
    filters,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from ...folder.callbacks import ChangeFolderCallback
from ...collection.callbacks import ChangeCollectionCallback


@dp.message(filters.Command('manage_item'))
async def change_item(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state_safe_clear(state)
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Manage folder'),
                callback_data=ChangeFolderCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Manage set / term'),
                callback_data=ChangeCollectionCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text=_('Choose item to manage'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
