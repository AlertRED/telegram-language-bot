from aiogram.filters.callback_data import CallbackData


class TaskCallback(CallbackData, prefix='task'):
    pass


class ShowStructureCallback(CallbackData, prefix='show_structure'):
    pass


class ChooseUserShowStructureCallback(
    CallbackData,
    prefix='choose_user_show_structure',
):
    pass


class ChooseOtherUserShowStructureCallback(
    CallbackData,
    prefix='choose_other_user_show_structure',
):
    pass


class LoadDataCallback(CallbackData, prefix='load_data'):
    pass


class ChooseUserLoadDataCallback(
    CallbackData,
    prefix='choose_user_load_data',
):
    pass


class ChooseOtherUserLoadDataCallback(
    CallbackData,
    prefix='choose_other_user_load_data',
):
    pass
