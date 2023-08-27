from aiogram import Router

from .handlers import manage
from .handlers import move_folder
from .handlers import delete_folder
from .handlers import rename_folder


router = Router()

router.include_routers(
    manage.router,
    move_folder.router,
    delete_folder.router,
    rename_folder.router,
)
