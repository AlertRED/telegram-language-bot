from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

from bot.instances import dispatcher as dp
from bot.handlers.settings.states import SettingsStates
from ..callbacks import (
    ChooseLanguageCallback,
    GoBackCallback,
)


@dp.message(filters.Command('settings'))
async def add_new_message(
    message: types.Message,
    state: FSMContext,
) -> None:
    await add_new(message, state)


@dp.callback_query(GoBackCallback.filter(), SettingsStates.choose_language)
async def add_new_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await add_new(callback.message, state)


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
