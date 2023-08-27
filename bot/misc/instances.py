"""Defined bot instances
"""

from arq.connections import RedisSettings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.utils.i18n import I18n

import config
from bot.misc.constants import DEFAULT_LOCALE
from scheduler.scheduler import ArqScheduler, Scheduler


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD,
)

i18n = I18n(
    path='./bot/locales',
    default_locale=DEFAULT_LOCALE,
    domain='messages',
)

__ = i18n.gettext


bot = Bot(
    token=config.API_TOKEN,
    parse_mode='HTML',
)
dispatcher = Dispatcher(storage=RedisStorage(redis))

arq_scheduler: Scheduler = ArqScheduler(
    RedisSettings(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        database=config.REDIS_DB,
        password=config.REDIS_PASSWORD,
    ),
)
