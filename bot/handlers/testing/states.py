from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class TestingStates(StatesGroup):
    choose_tool = State()
    show_structure_choose_user = State()
    show_structure_write_user_id = State()
    test_data_choose_user = State()
    test_data_write_user_id = State()
