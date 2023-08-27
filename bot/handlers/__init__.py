""" Module with main bot functional
"""
from .change_item import router as change_item_route
from .main_menu import router as main_menu_route
from .add_item import router as add_item_route
from .settings import router as settings_route
from .testing import router as testing_route
from .utils import router as utils_router
from .train import router as train_route


def get_routers():
    return [
        change_item_route.router,
        main_menu_route.router,
        add_item_route.router,
        settings_route.router,
        testing_route.router,
        utils_router.router,
        train_route.router,
    ]
