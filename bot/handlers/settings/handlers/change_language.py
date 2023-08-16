from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from bot.commands import get_commands

from bot.instances import (
    bot,
    dispatcher as dp,
)
from bot.handlers.support import state_safe_clear
from bot.handlers.settings.callbacks import (
    ChangeLanguageCallback,
    ChooseLanguageCallback,
    GoBackCallback,
)
from bot.handlers.settings.states import SettingsStates


@dp.callback_query(ChooseLanguageCallback.filter())
async def change_language(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await state_safe_clear(state)
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('English'),
                callback_data=ChangeLanguageCallback(lang='en').pack(),
            ),
            types.InlineKeyboardButton(
                text=_('Русский'),
                callback_data=ChangeLanguageCallback(lang='ru').pack(),
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_('Back'),
                callback_data=GoBackCallback().pack(),
            ),
        ],
    ]
    await callback.message.edit_text(
        text=_('Choose language'),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )
    await state.set_state(SettingsStates.choose_language)


@dp.callback_query(ChangeLanguageCallback.filter())
async def change_language(
    callback: types.CallbackQuery,
    callback_data: ChangeLanguageCallback,
    state: FSMContext,
) -> None:
    await state.update_data(locale=callback_data.lang)
    await bot.set_my_commands(
        commands=get_commands(callback_data.lang),
        language_code=callback.from_user.language_code,
        scope=types.bot_command_scope_chat.BotCommandScopeChat(
            chat_id=callback.message.chat.id,
        ),
    )
    await callback.message.edit_text(
        text=_('Language was changed!', locale=callback_data.lang),
    )
    await state_safe_clear(state)
