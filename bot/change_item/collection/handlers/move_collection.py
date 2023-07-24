from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from bot.utils.browse_folder import (
    start_browse as start_browse_folder,
)
from bot.utils.calbacks import FolderSelectCallback
from .manage import manage_collection
from ..states import ChangeCollectionStates
from ..callbacks import MoveCollectionCallback


router = Router()


@router.callback_query(
    MoveCollectionCallback.filter(F.sure == True),
)
async def move_collection_true(
    callback: types.CallbackQuery,
    callback_data: MoveCollectionCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        folder_id=callback_data.folder_id,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=(
            f'{state_data["collection_name"]} was moved to '
            f'{callback_data.folder_name}'
        ),
    )


@router.callback_query(
    MoveCollectionCallback.filter(F.sure == False),
)
async def move_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(MoveCollectionCallback.filter())
async def move_collection_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse_folder(callback)
    await state.set_state(ChangeCollectionStates.choose_folder_for_moving)


@router.callback_query(
    FolderSelectCallback.filter(),
    ChangeCollectionStates.choose_folder_for_moving,
)
async def move_collection_sure(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure wanna move '
            f'<u><b>{state_data["collection_name"]}</b></u>'
            f' into <u><b>{callback_data.folder_name or "Root"}</b></u>?'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=MoveCollectionCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=MoveCollectionCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.agree_moving)

