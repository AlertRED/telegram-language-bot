from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class MoveFolderStates(StatesGroup):
    choose_folder = State()
    agree = State()


class ChangeFolderStates(StatesGroup):
    choose_place = State()
    change_name = State()