import asyncio
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Optional
from contextlib import suppress
from arq import ArqRedis, create_pool
from arq.jobs import Job
from arq.connections import RedisSettings


FIND_DEFINITION_Q_NAME: str = 'find_definition'


class Scheduler(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def enqueue_job(
        self, task: Awaitable, q_name: str, delay: int,
    ) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    async def abort_job(self, job_id: str, q_name: str) -> None:
        raise NotImplementedError


class ArqScheduler(Scheduler):

    def __init__(self, redis_settings: RedisSettings) -> None:
        self.redis_settings: RedisSettings = redis_settings
        self.q_name_format = 'arq:{q_name}'
        self.pools = {}

    async def init_pool(self, *args):
        for q_name in args:
            self.pools[q_name] = await create_pool(
                self.redis_settings,
                default_queue_name=self.q_name_format.format(q_name=q_name),
            )

    def __get_queue(self, q_name: str) -> ArqRedis:
        queue = self.pools.get(q_name)
        if queue:
            return queue
        raise Exception("Queue is not initialized")

    async def enqueue_job(
        self, task_name: str, q_name: str, delay: int, **kwargs,
    ) -> int:
        queue = self.__get_queue(q_name)
        job = await queue.enqueue_job(
            function=task_name,
            _defer_by=delay,
            **kwargs,
        )
        return job.job_id

    async def abort_job(self, job_id: str, q_name) -> None:
        queue = self.__get_queue(q_name)
        with suppress(asyncio.TimeoutError):
            await Job(job_id, redis=queue).abort(timeout=0)
