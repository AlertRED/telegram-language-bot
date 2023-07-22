import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import (
    filters,
    types,
)

from config import API_TOKEN
from bot.handlers import (
    add_item,
    change_item,
    testing,
    train,
)
from bot.handlers.utils import browse_collection
from bot.handlers.utils import browse_folder
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
        f'/train - train words from set\n'
        f'/add_item - add new term, set or folder\n'
        f'/change_item - change term, set or folder\n',
    )


async def run():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Main menu'),
        types.BotCommand(
            command='add_item',
            description='Add new term, set or folder',
        ),
        types.BotCommand(
            command='train',
            description='Train words from set',
        ),
        types.BotCommand(
            command='change_item',
            description='Change term, set or folder',
        ),
        types.BotCommand(
            command='testing',
            description='Testing',
        ),
    ])
    dispatcher.include_routers(
        browse_folder.router,
        browse_collection.router,
        add_item.router,
        train.router,
        change_item.router,
        testing.router,
    )
    await dispatcher.start_polling(bot)
