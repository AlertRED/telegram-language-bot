from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.filters.callback_data import CallbackData


router = Router()


class ChangeFolderCallback(CallbackData, prefix='change_folder'):
    pass


class ChangeCollectionCallback(CallbackData, prefix='change_collection'):
    pass


@router.message(filters.Command('change_item'))
async def change_item(message: types.Message) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text='Change folder',
                callback_data=ChangeFolderCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Change collection',
                callback_data=ChangeCollectionCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Change term',
                callback_data=ChangeCollectionCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text='Choose item to change',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
