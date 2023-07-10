from aiogram import (
    Router,
    filters,
    types,
)

from bot.handlers.change_item.callbacks import (
    ChangeCollectionCallback,
    ChangeFolderCallback,
)
from .change_folder import router as change_folder_router
from .change_collection import router as change_collection_router


router = Router()
router.include_routers(
    change_folder_router,
    change_collection_router,
)


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
                text='Change set',
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
