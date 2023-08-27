from aiogram import Router

from .handlers import menu
from .handlers import change_language

router = Router()

router.include_routers(
    menu.router,
    change_language.router,
)
