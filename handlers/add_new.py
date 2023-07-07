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


@router.message(
    filters.Command('add_new'),
)
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
        # [types.InlineKeyboardButton(text='Go back')],
    ]
    await message.answer(
        text='What do you wonna add',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
