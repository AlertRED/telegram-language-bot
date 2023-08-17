from aiogram import types

from bot.instances import i18n


_ = i18n.gettext


def get_commands(locale: str):
    return [
        types.BotCommand(
            command='start',
            description=_(
                '🌱 Main menu',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='train',
            description=_(
                '🏋️ Train words from set',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='add_item',
            description=_(
                '✍️ Add new term, set or folder',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='manage_item',
            description=_(
                '🗂 Change term, set or folder',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='settings',
            description=_(
                '⚙️ Your settings',
                locale=locale,
            ),
        ),
    ]
