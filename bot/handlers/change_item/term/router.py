from aiogram import Router

from .handlers import manage
from .handlers import move_term
from .handlers import delete_term
from .handlers import change_name
from .handlers import change_definition


router = Router()

router.include_routers(
    manage.router,
    move_term.router,
    delete_term.router,
    change_name.router,
    change_definition.router,
)
