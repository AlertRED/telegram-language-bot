from aiogram import Router

from .handlers import menu
from .handlers import find_definition
from .handlers import simple_train


router = Router()

router.include_routers(
    menu.router,
    find_definition.router,
    simple_train.router,
)
