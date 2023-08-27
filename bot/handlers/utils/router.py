from aiogram import Router

from .handlers import browse_collection
from .handlers import browse_folder
from .handlers import browse_term


router = Router()

router.include_routers(
    browse_collection.router,
    browse_folder.router,
    browse_term.router,
)
