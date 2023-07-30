from aiogram import (
    filters,
    types,
)
from aiogram.utils.i18n import gettext as _

from bot.instances import (
    dispatcher,
    queue,
    bot,
)
from bot.handlers import (
    change_item,
    add_item,
    testing,
    train,
)
from bot.handlers.utils import (
    browse_collection,
    browse_folder,
    browse_term,
)
import database.dao as dao


@dispatcher.message(filters.Command('start'))
async def start_menu(message: types.Message) -> None:
    dao.register_user(message.from_user.id)
    await message.answer(
        text=_(
            'Hi, {username}!\n'
            '\nI\'ll help you to learn any language.'
            '\nBot commands:'
            '\n/start - main menu'
            '\n/train - train words from set'
            '\n/add_item - add new term, set or folder'
            '\n/manage_item - change term, set or folder'
        ).format(
            username=message.from_user.first_name,
        )
    )


async def run():
    dispatcher.include_routers(
        browse_folder.router,
        browse_collection.router,
        browse_term.router,
        add_item.router,
        train.router,
        change_item.router,
        testing.router,
    )
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Main menu'),
        types.BotCommand(
            command='add_item',
            description='Add new term, set or folder',
        ),
        types.BotCommand(
            command='train',
            description='Train words from set',
        ),
        types.BotCommand(
            command='manage_item',
            description='Change term, set or folder',
        ),
        types.BotCommand(
            command='testing',
            description='Testing',
        ),
    ])
    await queue.empty()
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
