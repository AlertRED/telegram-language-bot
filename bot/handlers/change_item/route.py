from aiogram import Router

from .menu import route as menu_router
from .term import route as term_router
from .folder import route as folder_router
from .collection import route as collection_router


router = Router()
router.include_routers(
    menu_router.router,
    term_router.router,
    folder_router.router,
    collection_router.router,
)
