"""Support functional for bot
"""

from typing import List
from aiogram import types
from aiogram.fsm.context import FSMContext

from .constants import PERMANENT_SAVED_KEYS_IN_STATE
from .instances import __


async def state_safe_clear(
    state: FSMContext,
    is_state: bool = True,
    is_data: bool = True,
    excluded_keys: list = None,
) -> None:
    """Clear state not fully

    :param state: State object
    :type state: FSMContext
    :param is_state: clear state or not, defaults to True
    :type is_state: bool, optional
    :param is_data: clear data or not, defaults to True
    :type is_data: bool, optional
    :param excluded_keys: which keys don't need to delete from data, defaults to None
    :type excluded_keys: list, optional
    """
    if is_state:
        await state.set_state(None)
    if is_data:
        state_data = await state.get_data()
        _excluded_keys = excluded_keys or [] + PERMANENT_SAVED_KEYS_IN_STATE
        save_data = {
            k: v
            for k, v in state_data.items()
            if k in _excluded_keys
        }
        await state.set_data(save_data)


def get_commands(locale: str) -> List[types.BotCommand]:
    """Get list of bot commands

    :param locale: 'en' or 'ru'
    :type locale: str
    :rtype: List[types.BotCommand]
    """
    return [
        types.BotCommand(
            command='start',
            description=__(
                '🌱 Main menu',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='train',
            description=__(
                '🏋️ Train words from set',
                locale=locale
            ),
        ),
        types.BotCommand(
            command='add_item',
            description=__(
                '✍️ Add new term, set or folder',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='manage_item',
            description=__(
                '🗂 Change term, set or folder',
                locale=locale,
            ),
        ),
        types.BotCommand(
            command='settings',
            description=__(
                '⚙️ Your settings',
                locale=locale,
            ),
        ),
    ]