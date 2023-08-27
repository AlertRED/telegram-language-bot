from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.handlers.utils.handlers.browse_collection import (
    browse as browse_collection,
)
from bot.handlers.utils.calbacks import CollectionSelectCallback
from ..states import ChangeCollectionStates
from ..controller import manage_collection
from ..callbacks import (
    ChangeCollectionCallback,
)


router = Router()


@router.callback_query(ChangeCollectionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse_collection(callback, state)
    await state.set_state(ChangeCollectionStates.manage_choose_place)


@router.callback_query(
    CollectionSelectCallback.filter(),
    ChangeCollectionStates.manage_choose_place,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
    )

