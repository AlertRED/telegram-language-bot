from aiogram import Router

from .handlers import manage
from .handlers import delete_collection
from .handlers import rename_collection
from .handlers import move_collection


router = Router()

router.include_routers(
    manage.router,
    move_collection.router,
    rename_collection.router,
    delete_collection.router,
)
