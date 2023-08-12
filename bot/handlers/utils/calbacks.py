from typing import Optional
from aiogram.filters.callback_data import CallbackData


class CollectionSelectCallback(CallbackData, prefix='bc_select_collection'):
    collection_id: int
    collection_name: str


class FolderChangedCallback(CallbackData, prefix='bc_change_folder'):
    folder_id: Optional[int] = None
    exclude_collection_ids: Optional[list] = None
    page: Optional[int] = 0


class FolderSelectCallback(CallbackData, prefix='bf_select_folder'):
    folder_id: Optional[int] = None
    folder_name: Optional[str] = None


class FolderChangeCallback(CallbackData, prefix='bf_change_folder'):
    folder_id: Optional[int] = None
    page: Optional[int] = 0
    is_root_returnable: bool


class TermSelectedCallback(CallbackData, prefix='bt_term_selected'):
    term_id: int


class ChangeCollectionCallback(CallbackData, prefix='bt_collection_changed'):
    collection_id: int
    page: int
