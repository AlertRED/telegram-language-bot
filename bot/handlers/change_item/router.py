from aiogram import Router

from .menu import router as menu_router
from .term import router as term_router
from .folder import router as folder_router
from .collection import router as collection_router


router = Router()
router.include_routers(
    menu_router.router,
    term_router.router,
    folder_router.router,
    collection_router.router,
)
