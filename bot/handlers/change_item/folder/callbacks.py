from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ChangeFolderCallback(CallbackData, prefix='change_folder'):
    pass


class ChangeFolderNameCallback(CallbackData, prefix='change_folder_name'):
    pass


class MoveFolderCallback(CallbackData, prefix='move_folder'):
    sure: Optional[bool] = None
    folder_id: Optional[int] = None
    folder_name: Optional[str] = None


class DeleteFolderCallback(CallbackData, prefix='delete_folder'):
    sure: Optional[bool] = None
