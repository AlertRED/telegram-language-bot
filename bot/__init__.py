import yaml
import logging
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n.middleware import FSMI18nMiddleware

import config
from bot.constants import LOCALES_LIST
from bot.instances import dispatcher as dp
from bot.instances import queue
from bot.instances import i18n
from bot.commands import get_commands
from bot.middlewares import LoggerMiddleware


def __setup_middlewares(dp: Dispatcher):
    i18n_middleware = FSMI18nMiddleware(i18n=i18n)
    dp.message.outer_middleware(i18n_middleware)
    dp.callback_query.outer_middleware(i18n_middleware)
    dp.poll_answer.outer_middleware(i18n_middleware)

    logger_middleware = LoggerMiddleware(logger=logging.getLogger('bot'))
    dp.message.outer_middleware(logger_middleware)
    dp.callback_query.outer_middleware(logger_middleware)
    dp.poll_answer.outer_middleware(logger_middleware)


def __setup_logger():
    if config.IS_DEVELOP:
        logging.basicConfig(level=logging.NOTSET)
    else:
        with open(config.LOGGING_CONFIG_PATH, 'r') as f:
            config_d = yaml.safe_load(f.read())
            logging.config.dictConfig(config_d)


async def __send_locales(bot: Bot):
    if not config.IS_DEVELOP:
        for locale in LOCALES_LIST:
            await bot.set_my_commands(
                commands=get_commands(locale),
                language_code=locale,
            )


async def run():
    from bot.instances import bot
    from bot import handlers

    await queue.empty()

    __setup_logger()
    __setup_middlewares(dp)

    await __send_locales(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
