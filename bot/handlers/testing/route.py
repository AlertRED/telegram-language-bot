from aiogram import Router

from .handlers import testing


router = Router()

router.include_routers(
    testing.router,
)
