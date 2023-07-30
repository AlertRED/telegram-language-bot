from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.handlers.add_item.callbacks import (
    AddingCollectionCallback,
    AddingFolderCallback,
    AddingTermCallback,
)
from .handlers.add_collection import router as add_collection_router
from .handlers.add_folder import router as add_folder_router
from .handlers.add_term import router as add_term_router


router = Router()
router.include_routers(
    add_collection_router,
    add_folder_router,
    add_term_router,
)


@router.message(filters.Command('add_item'))
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
