from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.handlers.settings.callbacks import ChangeLanguage, ChooseLanguage
from bot.handlers.settings.states import SettingsStates


@dp.callback_query(ChooseLanguage.filter())
async def change_language(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text=_('English'),
                callback_data=ChangeLanguage(lang='en').pack(),
            ),
            types.InlineKeyboardButton(
                text=_('Русский'),
                callback_data=ChangeLanguage(lang='ru').pack(),
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


@dp.callback_query(ChangeLanguage.filter())
async def change_language(
    callback: types.CallbackQuery,
    callback_data: ChangeLanguage,
    state: FSMContext,
) -> None:
    await state.update_data(locale=callback_data.lang)
    await callback.message.edit_text(
        text=_('Language was changed!'),
    )
