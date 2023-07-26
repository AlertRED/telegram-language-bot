from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ChangeTermNameCallback(CallbackData, prefix='change_term_name'):
    pass


class ChangeTermDefinitionCallback(
    CallbackData,
    prefix='change_term_definition',
):
    pass


class ChangeTermCallback(CallbackData, prefix='change_term'):
    collection_id: int
    collection_name: str


class MoveTermCallback(CallbackData, prefix='move_term'):
    sure: Optional[bool]
    collection_id: Optional[int]
    collection_name: Optional[str]


class DeleteTermCallback(CallbackData, prefix='delete_term'):
    sure: Optional[bool]