from logging import Logger
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggerMiddleware(BaseMiddleware):
    def __init__(self, logger: Logger) -> None:
        self.logger: Logger = logger

    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        try:
            result = await handler(event, data)
        except Exception:
            self.logger.exception(
                msg=(
                    ' | '.join(
                        [
                            f'user_id: {data.get("event_chat").id}',
                            f'event: {data.get("event_update").event_type}',
                            f'state: {await data.get("state").get_state()}',
                        ]
                    )
                )
            )
        else:
            self.logger.info(
                msg=(
                    ' | '.join(
                        [
                            f'user_id: {data.get("event_chat").id}',
                            f'event: {data.get("event_update").event_type}',
                            f'state: {await data.get("state").get_state()}',
                        ]
                    )
                )
            )
            return result
