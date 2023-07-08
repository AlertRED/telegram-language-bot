import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import (
    filters,
    types,
)

from config import API_TOKEN
from bot.handlers import (
    browse_folder,
    browse_collection,
    add_new,
    add_term,
    add_collection,
    add_folder,
)
import database.dao as dao


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(storage=MemoryStorage())


@dispatcher.message(filters.Command('start'))
async def start(
    message: types.Message,
) -> None:
    dao.register_user(message.from_user.id)
    await message.answer(
        text=f'Hi, {message.from_user.first_name}! '
        f'I\'ll help you to learn any language.\n\n'
        f'Bot commands:\n'
        f'/start - main menu\n'
        f'/add_item - add new term, set or folder',
    )


async def run():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Main menu'),
        types.BotCommand(
            command='add_item',
            description='Add new term, set or folder',
        ),
    ])
    dispatcher.include_routers(
        browse_folder.router,
        browse_collection.router,
        add_new.router,
        add_term.router,
        add_collection.router,
        add_folder.router,
    )
    await dispatcher.start_polling(bot)
