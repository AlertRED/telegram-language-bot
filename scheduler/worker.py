from bot.handlers.train.tasks import time_was_expired
from bot.misc import setup
from bot.misc import dispatcher
from .scheduler import FIND_DEFINITION_Q_NAME


async def startup(ctx):
    await setup(dispatcher)


class WorkerSettings:
    queue_name = f'arq:{FIND_DEFINITION_Q_NAME}'
    functions = [time_was_expired]
    allow_abort_jobs = True
    on_startup = startup
