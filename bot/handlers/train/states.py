from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class FindDefinitionStates(StatesGroup):
    choose_collection = State()
    try_guess = State()
    finished_train = State()


class SimpleTrainStates(StatesGroup):
    choose_collection = State()
    show_term = State()
    remind_term = State()
