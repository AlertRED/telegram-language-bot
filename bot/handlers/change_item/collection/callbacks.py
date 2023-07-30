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
    sure: Optional[bool] = None


class MoveCollectionCallback(CallbackData, prefix='move_collectioin'):
    sure: Optional[bool] = None
    folder_id: Optional[int] = None
    folder_name: Optional[str] = None
