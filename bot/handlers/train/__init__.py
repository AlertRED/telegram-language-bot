from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.handlers.train.callbacks import (
    FindDefinitionCallback,
    SimpleTrainCallback,
)
from .find_definition import router as find_definition_router
from .simple_train import router as simple_train_router

router = Router()
router.include_routers(
    find_definition_router,
    simple_train_router,
)


@router.message(filters.Command('train'))
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
