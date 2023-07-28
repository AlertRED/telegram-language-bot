from aiogram.filters.callback_data import CallbackData


class AddingTermCallback(CallbackData, prefix='adding_term'):
    pass


class SuggestionDefinitionChosenCallback(
    CallbackData,
    prefix='suggestion_definition_chosen_term',
):
    suggestion_number: int


class AddingCollectionCallback(CallbackData, prefix='adding_collection'):
    pass


class AddingFolderCallback(CallbackData, prefix='adding_folder'):
    pass
