from aiogram.filters.callback_data import CallbackData


class FindDefinitionCallback(CallbackData, prefix='find_definition'):
    pass


class NextTryCallback(CallbackData, prefix='next_try'):
    pass


class FinishTrainCallback(CallbackData, prefix='finish_train'):
    pass


class SimpleTrainCallback(CallbackData, prefix='simple_train'):
    pass


class RemindTermCallback(CallbackData, prefix='remind_term'):
    pass


class IKnowTermCallback(CallbackData, prefix='i_know_term'):
    pass
