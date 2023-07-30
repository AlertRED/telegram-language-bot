from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

from bot.instances import dispatcher as dp
from bot.handlers.settings.states import SettingsStates
from ..callbacks import ChooseLanguage


@dp.message(filters.Command('settings'))
async def add_new(
    message: types.Message,
    state: FSMContext,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('Change language'),
                callback_data=ChooseLanguage().pack(),
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
