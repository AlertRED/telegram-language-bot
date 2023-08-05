from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.add_item.callbacks import (
    AddingCollectionCallback,
    AddingFolderCallback,
    AddingTermCallback,
)


@dp.message(filters.Command('add_item'))
async def add_new(
    message: types.Message,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Add term'),
                callback_data=AddingTermCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Add set'),
                callback_data=AddingCollectionCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Add folder'),
                callback_data=AddingFolderCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text=_('Type item to add'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
