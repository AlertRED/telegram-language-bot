"""Bot middlewares
"""

from logging import Logger
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggerMiddleware(BaseMiddleware):
    """Middleware for logging
    """    
    def __init__(self, logger: Logger) -> None:
        self.logger: Logger = logger

    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        DEFAULT_VALUE = '-'
        event_update = data.get("event_update")
        state = data.get("state")

        user = data.get("event_from_user")
        user_id = user.id if user else DEFAULT_VALUE
        event_type = event_update.event_type if event_update else DEFAULT_VALUE
        current_state = await state.get_state() if state else DEFAULT_VALUE

        str_data = ' | '.join(
            [
                f'user_id: {user_id}',
                f'event: {event_type}',
                f'state: {current_state}',
            ],
        )
        try:
            result = await handler(event, data)
        except Exception:
            self.logger.exception(msg=str_data)
        else:
            self.logger.info(msg=str_data)
            return result
