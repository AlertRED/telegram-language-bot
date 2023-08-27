from typing import Callable
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.misc.support import state_safe_clear
from database import dao
from .states import (
    CreateCollectionStates, CreateFolderStates, CreateTermStates,
)


async def write_collection_name(
    foo: Callable,
    state: FSMContext,
) -> None:
    await foo(text=_('Write set name'))
    await state.set_state(CreateCollectionStates.choose_name)


async def write_folder_name(
    foo: Callable,
    state: FSMContext,
) -> None:
    await foo(text=_('Write folder name'))
    await state.set_state(CreateFolderStates.choose_name)


async def add_term(
    foo: Callable,
    state: FSMContext,
    telegram_user_id: int,
) -> None:
    state_data = await state.get_data()
    dao.create_term(
        telegram_user_id,
        state_data.get('collection_id'),
        state_data.get('term_name'),
        state_data.get('term_description'),
    )
    await foo(
        text=_(
            'Term added into {collection_name}\n'
            'Term: <b><u>{term_name}</u></b>\n'
            'Description: {term_description}'
        ).format(
            collection_name=state_data.get('collection_name'),
            term_name=state_data.get('term_name'),
            term_description=state_data.get('term_description'),
        ),
    )
    await state_safe_clear(state,)


async def write_term_name(
    foo: Callable,
    state: FSMContext,
) -> None:
    await foo(text=_('Write term'))
    await state.set_state(CreateTermStates.write_term)
