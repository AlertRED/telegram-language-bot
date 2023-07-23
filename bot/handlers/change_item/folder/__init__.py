from aiogram import Router

from .manage import router as manage_router
from .delete_folder import router as delete_folder_router
from .rename_folder import router as rename_folder_router
from .move_folder import router as move_folder_router


router = Router()
router.include_routers(
    manage_router,
    delete_folder_router,
    rename_folder_router,
    move_folder_router,
)
