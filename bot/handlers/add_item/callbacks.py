from aiogram.filters.callback_data import CallbackData


class AddTermCallback(CallbackData, prefix='add_term'):
    pass


class SuggestionDefinitionChosenCallback(
    CallbackData,
    prefix='suggestion_definition_chosen_term',
):
    suggestion_number: int


class AddCollectionCallback(CallbackData, prefix='add_collection'):
    pass


class AddingFolderCallback(CallbackData, prefix='add_folder'):
    pass
