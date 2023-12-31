from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.support import state_safe_clear
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from ..states import ChangeTermStates
from ..callbacks import MoveTermCallback
from ..controller import choose_collection


router = Router()


@router.callback_query(MoveTermCallback.filter())
async def choose_collection_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await state.update_data(
        exclude_collection_ids=[state_data.get('collection_id')],
    )
    await choose_collection(callback, state)


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
        term_id=state_data.get('term_id'),
        collection_id=state_data.get('collection_id'),
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=_(
            '<u><b>{term_name}</b></u> was moved to '
            '{collection_name}'
        ).format(
            term_name=state_data.get('term_name'),
            collection_name=callback_data.collection_name,
        ),
    )
    await state_safe_clear(state)


@router.callback_query(MoveTermCallback.filter(F.sure == False))
async def move_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(
    CollectionSelectCallback.filter(),
    ChangeTermStates.choose_collection_for_moving,
)
async def move_collection_sure(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
):
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
    )
    state_data = await state.get_data()

    term = dao.get_term(
        term_name=state_data.get('term_name'),
        collection_id=state_data.get('collection_id'),
    )
    if term:
        await callback.message.answer(
            text=(
                'The term <b><u>{term_name}</u></b> is already exists'
                ' in the collection {collection_name}!'
            ).format(
                term_name=state_data.get('term_name'),
                collection_name=state_data.get('collection_name'),
            ),
        )
        await choose_collection(callback, state)
        return

    await callback.message.edit_text(
        text=_(
            'Are you sure wanna move '
            '<u><b>{term_name}</b></u>'
            ' into <u><b>{collection_name}</b></u>?'
        ).format(
            term_name=state_data.get('term_name'),
            collection_name=callback_data.collection_name,
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Yes'),
                        callback_data=MoveTermCallback(
                            sure=True,
                            collection_id=callback_data.collection_id,
                            collection_name=callback_data.collection_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('No'),
                        callback_data=MoveTermCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.agree_moving)
