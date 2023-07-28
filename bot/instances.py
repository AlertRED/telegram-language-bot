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

import config


logging.basicConfig(level=logging.INFO)
redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD,
)

bot = Bot(token=config.API_TOKEN)
dispatcher = Dispatcher(storage=RedisStorage(redis))
queue = Queue(connection=redis)
