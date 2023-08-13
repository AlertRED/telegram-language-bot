from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram import (
    types,
    filters,
)

import database.dao as dao
from bot.instances import (
    DEFAULT_LOCALE,
    dispatcher as dp,
)
from ..states import MainMenuStates


@dp.message(filters.Command('start'))
async def start_menu(
    message: types.Message,
    state: FSMContext,
) -> None:
    dao.register_user(message.from_user.id)
    await state.update_data(locale=DEFAULT_LOCALE)
    await message.answer(
        text=_(
            'Hi, {username}!'
            '\nI\'ll help you to learn any language.'
            '\n\nBot commands:'
            '\n/train - 🏋️ train words from set'
            '\n/add_item - ✍️ add new term, set or folder'
            '\n/manage_item - 🗂 change term, set or folder'
            '\n/settings - ⚙️ your settings'
        ).format(
            username=message.from_user.first_name,
        )
    )
    await state.set_state(MainMenuStates.main_menu)
