from aiogram import Router

from .manage import router as manage_router
from .change_name import router as change_name_router


router = Router()
router.include_routers(
    manage_router,
    change_name_router,
)
