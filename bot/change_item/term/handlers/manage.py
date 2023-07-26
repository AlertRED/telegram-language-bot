from aiogram import (
    types,
    Router,
)
from aiogram.fsm.context import FSMContext

import database.dao as dao
from bot.change_item.collection.handlers.manage import manage_collection
from bot.utils.browse_term import CollectionIsEmptyException, start_browse as start_browse_term
from bot.utils.calbacks import TermSelectedCallback
from ..states import ChangeTermStates
from ..callbacks import (
    ChangeTermCallback,
    ChangeTermNameCallback,
    ChangeTermDefinitionCallback,
    DeleteTermCallback,
    MoveTermCallback,
)


router = Router()


@router.callback_query(ChangeTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    callback_data: ChangeTermCallback,
    state: FSMContext,
) -> None:
    try:
        await start_browse_term(
            callback,
            callback_data.collection_id,
        )
        await state.set_state(ChangeTermStates.manage_choose_term)
    except CollectionIsEmptyException:
        await manage_collection(
            callback.message.edit_text,
            state=state,
            additional_text=(
                f'<u><b>{callback_data.collection_name}</b></u> '
                f'doesn\'t have terms yet.'
            ),
        )


@router.callback_query(
    TermSelectedCallback.filter(),
    ChangeTermStates.manage_choose_term,
)
async def choose_collection(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    term = dao.get_term(callback_data.term_id)
    await state.update_data(
        term_id=callback_data.term_id,
        term_name=term.name,
        term_description=term.description,
    )

    await callback.message.edit_text(
        text=(
            f'<u><b>{term.name}</b></u> - {term.description}'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Change name',
                        callback_data=ChangeTermNameCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Change definition',
                        callback_data=ChangeTermDefinitionCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Delete term',
                        callback_data=DeleteTermCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Move term',
                        callback_data=MoveTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.manage_choose_option)
