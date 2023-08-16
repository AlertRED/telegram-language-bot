from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class CreateTermStates(StatesGroup):
    choose_place = State()
    write_term = State()
    write_description = State()


class CreateFolderStates(StatesGroup):
    choose_place = State()
    choose_name = State()


class CreateCollectionStates(StatesGroup):
    choose_place = State()
    choose_name = State()
