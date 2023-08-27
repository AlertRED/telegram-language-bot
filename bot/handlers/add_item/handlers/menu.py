from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.misc.support import state_safe_clear
from bot.handlers.add_item.callbacks import (
    AddCollectionCallback,
    AddingFolderCallback,
    AddTermCallback,
)


router = Router()


@router.message(filters.Command('add_item'))
async def add_new(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state_safe_clear(state)
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Add term'),
                callback_data=AddTermCallback().pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Add set'),
                callback_data=AddCollectionCallback().pack(),
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
