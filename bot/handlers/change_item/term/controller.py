
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.handlers.utils.handlers import browse_collection
from bot.handlers.change_item.term.states import ChangeTermStates


async def write_new_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await message.edit_text(
        text=_(
            'Write new definition'
            '(old definition is {term_description}):'
        ).format(
            term_description=state_data.get('term_description'),
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_definition)


async def write_term_name(
    foo: callable,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    await foo(
        text=_(
            'Write new name (old name is {term_name}):'
        ).format(
            term_name=state_data.get('term_name'),
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeTermStates.change_name)


async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await browse_collection(callback, state)
    await state.set_state(ChangeTermStates.choose_collection_for_moving)
