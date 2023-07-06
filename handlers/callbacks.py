from aiogram.filters.callback_data import CallbackData
from typing import (
    Optional,
)


class AddTermCallback(CallbackData, prefix='add_term'):
    pass


class SelectedFolderCallback(CallbackData, prefix='selected_folder'):
    folder_id: Optional[int]
    page: Optional[int]


class SelectedCollectionCallback(CallbackData, prefix='selected_collection'):
    collection_name: str
    collection_id: int
