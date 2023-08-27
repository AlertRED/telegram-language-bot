from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from .callbacks import ChooseLanguageCallback
from .states import SettingsStates


async def add_new(
    message: types.Message,
    state: FSMContext,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Change language'),
                callback_data=ChooseLanguageCallback().pack(),
            ),
        ],
    ]
    await message.answer(
        text=_('Settings'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
    await state.set_state(SettingsStates.settings)
