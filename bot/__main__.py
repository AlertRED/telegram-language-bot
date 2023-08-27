"""Main module of bot app
"""

import asyncio
from aiogram import Bot

import config
from bot.misc.support import get_commands
from bot.handlers import get_routers
from bot.misc import (
    setup,
    constants,
    dispatcher,
)


async def send_commands(bot: Bot):
    """Send bot commands to telegram

    :param bot: Bot object
    :type bot: Bot
    """

    if not config.IS_DEVELOP:
        for locale in constants.LOCALES_LIST:
            await bot.set_my_commands(
                commands=get_commands(locale),
                language_code=locale,
            )


async def main():
    """Main function to start bot
    """    
    from bot.misc.instances import bot
    dispatcher.include_routers(*get_routers())
    await setup(dispatcher)
    await send_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
