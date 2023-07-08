from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.filters.callback_data import CallbackData


router = Router()


class AddingTermCallback(CallbackData, prefix='adding_term'):
    pass


class AddingCollectionCallback(CallbackData, prefix='adding_collection'):
    pass


class AddingFolderCallback(CallbackData, prefix='adding_folder'):
    pass


@router.message(filters.Command('add_item'))
async def add_new(
    message: types.Message,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text='Add term',
                callback_data=AddingTermCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Add set',
                callback_data=AddingCollectionCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Add folder',
                callback_data=AddingFolderCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text='Type item to add',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
