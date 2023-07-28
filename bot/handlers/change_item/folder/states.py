from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class ChangeFolderStates(StatesGroup):
    manage_choose_place = State()
    manage_choose_option = State()
    option_change_name = State()
    option_moving = State()
    choose_folder_for_moving = State()
    agree_moving = State()
    agree_delete = State()
