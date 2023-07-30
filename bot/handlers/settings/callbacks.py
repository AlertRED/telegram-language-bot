from aiogram.filters.callback_data import CallbackData


class ChooseLanguage(CallbackData, prefix='choose_language'):
    pass


class ChangeLanguage(CallbackData, prefix='change_language'):
    lang: str
