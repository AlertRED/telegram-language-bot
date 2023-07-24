from aiogram import Router

from .handlers.manage import router as manage_router
from .handlers.delete_folder import router as delete_folder_router
from .handlers.rename_folder import router as rename_folder_router
from .handlers.move_folder import router as move_folder_router


router = Router()
router.include_routers(
    manage_router,
    delete_folder_router,
    rename_folder_router,
    move_folder_router,
)
