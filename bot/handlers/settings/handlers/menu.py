from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.fsm.context import FSMContext
from bot.handlers.settings.controller import add_new

from bot.handlers.settings.states import SettingsStates
from ..callbacks import GoBackCallback


router = Router()


@router.message(filters.Command('settings'))
async def add_new_message(
    message: types.Message,
    state: FSMContext,
) -> None:
    await add_new(message, state)


@router.callback_query(GoBackCallback.filter(), SettingsStates.choose_language)
async def add_new_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await add_new(callback.message, state)
