from aiogram import Router

from .handlers import menu


router = Router()

router.include_routers(
    menu.router,
)
