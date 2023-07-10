from aiogram.filters.callback_data import CallbackData


class AddingTermCallback(CallbackData, prefix='adding_term'):
    pass


class AddingCollectionCallback(CallbackData, prefix='adding_collection'):
    pass


class AddingFolderCallback(CallbackData, prefix='adding_folder'):
    pass
