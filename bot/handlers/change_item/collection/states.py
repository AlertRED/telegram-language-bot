from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class MoveCollectionsStates(StatesGroup):
    choose_folder = State()
    agree = State()


class ChangeCollectionStates(StatesGroup):
    choose_place = State()
    change_name = State()