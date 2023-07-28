from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import DeleteTermCallback
import database.dao as dao


router = Router()


@router.callback_query(DeleteTermCallback.filter(F.sure == False))
async def delete_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(DeleteTermCallback.filter(F.sure == True))
async def delete_term_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_term(state_data['term_id'])
    additional_text = (
        f'Term <u><b>{state_data["term_name"]}</b></u>'
        f' deleted succesfully!'
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=additional_text,
    )


@router.callback_query(DeleteTermCallback.filter())
async def delete_term_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure you wanna delete '
            f'<u><b>{state_data.get("term_name")}</b></u>?\n'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=DeleteTermCallback(
                            sure=True,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=DeleteTermCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.agree_delete)
