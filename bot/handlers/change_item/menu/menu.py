from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from ..folder.callbacks import ChangeFolderCallback
from ..collection.callbacks import ChangeCollectionCallback


@dp.message(filters.Command('manage_item'))
async def change_item(message: types.Message) -> None:
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
