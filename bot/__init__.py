from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.instances import queue


@dp.message(filters.Command('start'))
async def start_menu(message: types.Message) -> None:
    dao.register_user(message.from_user.id)
    await message.answer(
        text=_(
            'Hi, {username}!'
            '\nI\'ll help you to learn any language.'
            '\n\nMy commands:'
            '\n/start - 🌱 main menu'
            '\n/train - 🧠 train words from set'
            '\n/add_item - 📓 add new term, set or folder'
            '\n/manage_item - 🗂 change term, set or folder'
            '\n/settings - ⚙️ your settings'
        ).format(
            username=message.from_user.first_name,
        )
    )


async def run():
    from bot.instances import bot

    await bot.set_my_commands([
        types.BotCommand(command='start', description='🌱 Main menu'),
        types.BotCommand(
            command='train',
            description='🧠 Train words from set',
        ),
        types.BotCommand(
            command='add_item',
            description='📓 Add new term, set or folder',
        ),
        types.BotCommand(
            command='manage_item',
            description='🗂 Change term, set or folder',
        ),
        types.BotCommand(
            command='settings',
            description='⚙️ Your settings',
        ),
    ])
    await queue.empty()
    await bot.delete_webhook(drop_pending_updates=True)
    from bot import handlers
    await dp.start_polling(bot)
