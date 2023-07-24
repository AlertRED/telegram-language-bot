from aiogram import Router

from .handlers.manage import router as manage_router
from .handlers.delete_collection import router as delete_collection_router
from .handlers.move_collection import router as move_collection_router
from .handlers.rename_collection import router as rename_collection_router


router = Router()
router.include_routers(
    manage_router,
    rename_collection_router,
    delete_collection_router,
    move_collection_router,
)
