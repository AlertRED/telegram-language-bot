from aiogram.filters.callback_data import CallbackData


class ChangeTermNameCallback(CallbackData, prefix='change_term_name'):
    pass


class ChangeTermCallback(CallbackData, prefix='change_term'):
    collection_id: int
