from aiogram import (
    Router,
    types,
)
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from aiogram.fsm.context import FSMContext

from .callbacks import (
    ChangeTermCallback,
    ChangeTermNameCallback,
)
from bot.handlers.utils.browse_term import start_browse as start_browse_term
from bot.handlers.utils.calbacks import TermSelectedCallback
import database.dao as dao
from .change_name import router as change_name_router


router = Router()
router.include_router(change_name_router)


class ChangeTermStates(StatesGroup):
    choose_folder = State()
    change_name = State()


@router.callback_query(ChangeTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    callback_data: ChangeTermCallback,
    state: FSMContext,
) -> None:
    await start_browse_term(callback, callback_data.collection_id)
    await state.set_state(ChangeTermStates.choose_folder)


@router.callback_query(
    TermSelectedCallback.filter(),
    ChangeTermStates.choose_folder,
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
            ],
        ),
    )
