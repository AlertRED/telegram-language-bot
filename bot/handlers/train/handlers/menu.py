from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.train.callbacks import (
    FindDefinitionCallback,
    SimpleTrainCallback,
)


@dp.message(filters.Command('train'))
async def train_message(message: types.Message) -> None:
    await train(message)


async def train(message: types.Message) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Find definition'),
                callback_data=FindDefinitionCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Simple train'),
                callback_data=SimpleTrainCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text=_('Choose train type'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
