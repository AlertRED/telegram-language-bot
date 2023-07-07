import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from handlers import (
    browse_folder,
    browse_collection,
    add_new,
    add_term,
    add_collection,
    add_folder,
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(storage=MemoryStorage())


async def main():
    await bot.set_my_commands([
        types.BotCommand(command='add_new', description='Add new'),
        # types.BotCommand(command='train', description='Train'),
        # types.BotCommand(command='change_item', description='Change item'),
        # types.BotCommand(command='settings', description='Settings'),
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


if __name__ == '__main__':
    asyncio.run(main())
