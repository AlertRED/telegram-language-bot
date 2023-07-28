from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ChangeCollectionCallback(CallbackData, prefix='change_collection'):
    pass


class ChangeCollectionNameCallback(
    CallbackData,
    prefix='change_collection_name',
):
    pass


class DeleteCollectionCallback(CallbackData, prefix='delete_collection'):
    sure: Optional[bool]


class MoveCollectionCallback(CallbackData, prefix='move_collectioin'):
    sure: Optional[bool]
    folder_id: Optional[int]
    folder_name: Optional[str]
