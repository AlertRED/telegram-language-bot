from aiogram import Router

from .manage import router as manage_router
from .move_term import router as move_term_router
from .change_name import router as change_name_router
from .change_definition import router as change_definition_router
from .delete_term import router as delete_term_router


router = Router()
router.include_routers(
    manage_router,
    move_term_router,
    change_name_router,
    change_definition_router,
    delete_term_router,
)
