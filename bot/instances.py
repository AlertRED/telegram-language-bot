import logging
from rq import Queue
from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.fsm.storage.redis import (
    Redis,
    RedisStorage,
)
from aiogram.utils import i18n

import config


logging.basicConfig(level=logging.INFO)
redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD,
)


i18n_middleware = i18n.middleware.FSMI18nMiddleware(
    i18n=i18n.I18n(
        path='./bot/locales',
        default_locale='ru',
        domain='messages',
    ),
)
bot = Bot(token=config.API_TOKEN)
dispatcher = Dispatcher(storage=RedisStorage(redis))
dispatcher.message.outer_middleware(i18n_middleware)
queue = Queue(connection=redis)
