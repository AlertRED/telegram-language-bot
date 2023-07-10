from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ChangeCollectionCallback(CallbackData, prefix='change_collection'):
    pass


class ChangeCollectionNameCallback(
    CallbackData,
    prefix='change_collection_name',
):
    pass


class MoveCollectionCallback(CallbackData, prefix='move_collectioin'):
    sure: Optional[bool]
    folder_id: Optional[int]
    folder_name: Optional[str]


class DeleteCollectionCallback(CallbackData, prefix='delete_collection'):
    sure: Optional[bool]


class ChangeFolderCallback(CallbackData, prefix='change_folder'):
    pass


class ChangeFolderNameCallback(CallbackData, prefix='change_folder_name'):
    pass


class MoveFolderCallback(CallbackData, prefix='move_folder'):
    sure: Optional[bool]
    folder_id: Optional[int]
    folder_name: Optional[str]


class DeleteFolderCallback(CallbackData, prefix='delete_folder'):
    sure: Optional[bool]
