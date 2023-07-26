from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import (
    filters,
    types,
)

from bot.add_item import routers
from bot.testing import testing
from bot import (
    change_item,
    train,
)
from bot.utils import (
    browse_collection,
    browse_folder,
    browse_term,
)
import database.dao as dao


dispatcher = Dispatcher(storage=MemoryStorage())
dispatcher.include_routers(
    browse_folder.router,
    browse_collection.router,
    browse_term.router,
    routers.router,
    train.router,
    change_item.router,
    testing.router,
)


@dispatcher.message(filters.Command('start'))
async def start(message: types.Message) -> None:
    dao.register_user(message.from_user.id)
    await message.answer(
        text=f'Hi, {message.from_user.first_name}! '
        f'I\'ll help you to learn any language.\n\n'
        f'Bot commands:\n'
        f'/start - main menu\n'
        f'/train - train words from set\n'
        f'/add_item - add new term, set or folder\n'
        f'/manage_item - change term, set or folder\n',
    )
