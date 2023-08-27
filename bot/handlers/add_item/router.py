from aiogram import Router

from .handlers import menu
from .handlers import add_term
from .handlers import add_folder
from .handlers import add_collection


router = Router()
router.include_routers(
    menu.router,
    add_term.router,
    add_folder.router,
    add_collection.router,
)
