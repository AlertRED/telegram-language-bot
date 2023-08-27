from aiogram import Router
from .handlers import main_menu

router = Router()
router.include_routers(
    main_menu.router,
)
