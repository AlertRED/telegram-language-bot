from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class ChangeTermStates(StatesGroup):
    manage_choose_term = State()
    manage_choose_option = State()
    change_name = State()
    change_definition = State()
    choose_collection_for_moving = State()
    agree_moving = State()
