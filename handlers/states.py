from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class AddNewState(StatesGroup):
    add_term = State()
    add_collection = State()
    add_folder = State()


class AddNewTermState(StatesGroup):
    add_term = State()
    add_description = State()
