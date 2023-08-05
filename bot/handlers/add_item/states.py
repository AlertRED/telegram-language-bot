from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class CreateTermStates(StatesGroup):
    choose_place = State()
    choose_term = State()
    choose_description = State()


class CreateFolderStates(StatesGroup):
    choose_place = State()
    choose_name = State()


class CreateCollectionStates(StatesGroup):
    choose_place = State()
    choose_name = State()
