from aiogram import Router
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

from .manage import manage_collection
from .states import ChangeCollectionStates
from .callbacks import ChangeCollectionNameCallback
import database.dao as dao


router = Router()


@router.callback_query(ChangeCollectionNameCallback.filter())
async def change_collection_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=f'Write new name (old name {state_data["collection_name"]}):',
        parse_mode='html',
    )
    await state.set_state(ChangeCollectionStates.change_name)


@router.message(
    ChangeCollectionStates.change_name,
)
async def change_collection_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        collection_name=message.text,
    )
    await state.update_data(
        collection_name=message.text,
    )
    await manage_collection(
        message.answer,
        state,
        additional_text=(
            f'Collection name <u><b>{state_data["collection_name"]}</b></u> '
            f'changed to <u><b>{message.text}</b></u>'
        ),
    )
