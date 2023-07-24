from aiogram import Router
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from bot.utils.browse_collection import (
    start_browse as start_browse_collection,
)
from bot.utils.calbacks import CollectionSelectCallback
from bot.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import MoveTermCallback


router = Router()


@router.callback_query(
    MoveTermCallback.filter(F.sure == True),
)
async def move_collection_true(
    callback: types.CallbackQuery,
    callback_data: MoveTermCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_term(
        term_id=state_data['term_id'],
        collection_id=callback_data.collection_id,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=(
            f'{state_data["term_name"]} was moved to '
            f'{callback_data.collection_name}'
        ),
    )


@router.callback_query(
    MoveTermCallback.filter(F.sure == False),
)
async def move_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(MoveTermCallback.filter())
async def move_term_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse_collection(callback)
    await state.set_state(ChangeTermStates.choose_collection_for_moving)


@router.callback_query(
    CollectionSelectCallback.filter(),
    ChangeTermStates.choose_collection_for_moving,
)
async def move_collection_sure(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure wanna move '
            f'<u><b>{state_data["term_name"]}</b></u>'
            f' into <u><b>{callback_data.collection_name}</b></u>?'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=MoveTermCallback(
                            sure=True,
                            collection_id=callback_data.collection_id,
                            collection_name=callback_data.collection_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=MoveTermCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.agree_moving)
