from rq import Queue
from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.fsm.storage.redis import (
    Redis,
    RedisStorage,
)
from aiogram.utils.i18n import I18n

import config
from bot.constants import DEFAULT_LOCALE


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

bot = Bot(
    token=config.API_TOKEN,
    parse_mode='HTML',
)
dispatcher = Dispatcher(storage=RedisStorage(redis))
queue = Queue(connection=redis)
