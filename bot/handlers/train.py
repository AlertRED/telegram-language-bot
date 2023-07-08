from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.filters.callback_data import CallbackData


router = Router()


class FindDefinitionCallback(CallbackData, prefix='find_definition'):
    pass


@router.message(filters.Command('train'))
async def train(message: types.Message) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text='Find definition',
                callback_data=FindDefinitionCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text='Choose train type',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
