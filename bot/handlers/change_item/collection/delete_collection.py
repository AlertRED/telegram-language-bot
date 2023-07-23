from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

from .manage import manage_collection
from .states import ChangeCollectionStates
from .callbacks import DeleteCollectionCallback
import database.dao as dao


router = Router()


@router.callback_query(DeleteCollectionCallback.filter(F.sure == False))
async def delete_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(DeleteCollectionCallback.filter(F.sure == True))
async def delete_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_collection(state_data['collection_id'])
    await callback.message.answer(
        text=(
            f'Collection <u><b>{state_data["collection_name"]}</b></u>'
            f' deleted succesfully!\n\n'
        ),
        parse_mode='html',
    )


@router.callback_query(DeleteCollectionCallback.filter())
async def delete_collection_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure you wanna delete '
            f'<u><b>{state_data.get("collection_name")}</b></u>?\n'
            f'All terms inside will be deleted too!'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=DeleteCollectionCallback(
                            sure=True,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=DeleteCollectionCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.change_name)
