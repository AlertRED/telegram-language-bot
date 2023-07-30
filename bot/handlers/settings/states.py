from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class SettingsStates(StatesGroup):
    settings = State()
    choose_language = State()
