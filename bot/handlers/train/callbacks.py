from typing import Optional
from aiogram.filters.callback_data import CallbackData


class FindDefinitionCallback(CallbackData, prefix='find_definition'):
    pass


class SimpleTrainCallback(CallbackData, prefix='simple_train'):
    pass


class FinishGameCallback(CallbackData, prefix='finish_find_definition'):
    win_count: int
    lose_count: int


class TryGuessCallback(CallbackData, prefix='try_guess'):
    term_name: Optional[str]
    term_description: Optional[str]
    term_description_guess: Optional[str]


class FinishGameCallback(CallbackData, prefix='finish_find_definition'):
    win_count: int
    lose_count: int


class RemindTermCallback(CallbackData, prefix='remind_term'):
    pass


class IKnowTermCallback(CallbackData, prefix='i_know_term'):
    pass