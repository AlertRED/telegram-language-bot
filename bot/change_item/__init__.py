from aiogram import (
    Router,
    filters,
    types,
)

from .folder.callbacks import ChangeFolderCallback
from .collection.callbacks import ChangeCollectionCallback
from .term.routers import router as change_term_router
from .folder.routers import router as change_folder_router
from .collection.routers import router as change_collection_router


router = Router()
router.include_routers(
    change_term_router,
    change_folder_router,
    change_collection_router,
)


@router.message(filters.Command('manage_item'))
async def change_item(message: types.Message) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text='Manage folder',
                callback_data=ChangeFolderCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Manage set / term',
                callback_data=ChangeCollectionCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text='Choose item to manage',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
