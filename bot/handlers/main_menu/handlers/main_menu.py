import json
from aiogram import (
    filters,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.router import Router

import database.dao as dao
from bot.misc.support import state_safe_clear
from bot.misc.instances import (
    DEFAULT_LOCALE,
)

from ..states import MainMenuStates


router = Router()


def load_oxford3000(telegram_user_id: int):
    with open('assets/dictionary.json', 'r') as file:
        dictionary = json.load(file)
    dao.add_dict(telegram_user_id, dictionary, 'Oxford 3000')


@router.message(filters.Command('start'))
async def start_menu(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state_safe_clear(state)
    success = dao.register_user(message.from_user.id)
    if success:
        load_oxford3000(message.from_user.id)
        await message.answer(
            text=_(
                'You are registered!'
                'You already have folder "Oxford 3000" as my gift to you :)'
                'The Oxford 3000 is the list of the 3000 most important words '
                'to learn in English, from A1 to B2 level. '
            ),
        )

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
