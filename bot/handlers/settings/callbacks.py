from aiogram.filters.callback_data import CallbackData


class ChooseLanguageCallback(CallbackData, prefix='choose_language'):
    pass


class ChangeLanguageCallback(CallbackData, prefix='change_language'):
    lang: str


class GoBackCallback(CallbackData, prefix='go_back'):
    pass
