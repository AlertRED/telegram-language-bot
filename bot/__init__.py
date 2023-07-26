import logging
from aiogram import Bot, types
from aiogram import (
    types,
)

from config import API_TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)


async def run():
    from bot.router import dispatcher
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
            command='manage_item',
            description='Change term, set or folder',
        ),
        types.BotCommand(
            command='testing',
            description='Testing',
        ),
    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
