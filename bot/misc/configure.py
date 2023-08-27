"""File with setup bot functions
"""

import yaml
import logging
import logging.config
from aiogram import Dispatcher
from aiogram.utils.i18n.middleware import FSMI18nMiddleware

import config
from scheduler import FIND_DEFINITION_Q_NAME

from .middlewares import LoggerMiddleware
from .instances import i18n, arq_scheduler


def __setup_middlewares(dp: Dispatcher):
    """Connect middlewares to dp

    :param dp: dispatcher object
    :type dp: Dispatcher
    """

    i18n_middleware = FSMI18nMiddleware(i18n=i18n)
    i18n_middleware.setup(dp)
    dp.message.outer_middleware(i18n_middleware)
    dp.callback_query.outer_middleware(i18n_middleware)
    dp.poll_answer.outer_middleware(i18n_middleware)

    logger_middleware = LoggerMiddleware(logger=logging.getLogger('bot'))
    dp.message.outer_middleware(logger_middleware)
    dp.callback_query.outer_middleware(logger_middleware)
    dp.poll_answer.outer_middleware(logger_middleware)


def __setup_logger():
    """Load logging
    """

    if config.IS_DEVELOP:
        logging.basicConfig(level=logging.NOTSET)
    else:
        with open(config.LOGGING_CONFIG_PATH, 'r') as f:
            config_d = yaml.safe_load(f.read())
            logging.config.dictConfig(config_d)


async def setup(dp: Dispatcher):
    """Setup bot app

    :param dp: dispatcher object
    :type dp: Dispatcher
    """

    __setup_logger()
    __setup_middlewares(dp)
    await arq_scheduler.init_pool(FIND_DEFINITION_Q_NAME)
