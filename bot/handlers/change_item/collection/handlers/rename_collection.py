from typing import Callable

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.support import state_safe_clear
from .manage import manage_collection
from ..states import ChangeCollectionStates
from ..callbacks import ChangeCollectionNameCallback


@dp.callback_query(ChangeCollectionNameCallback.filter())
async def write_collection_name_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await write_collection_name(callback.message.edit_text, state)


async def write_collection_name(
    foo: Callable,
    state: FSMContext,
):
    state_data = await state.get_data()
    await foo(
        text=_(
            'Write new name (old name {collection_name}):'
        ).format(collection_name=state_data.get('collection_name')),
        parse_mode='html',
    )
    await state.set_state(ChangeCollectionStates.option_change_name)


@dp.message(
    ChangeCollectionStates.option_change_name,
)
async def change_collection_name(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(collection_new_name=message.text)
    state_data = await state.get_data()
    collection = dao.get_collection(
        telegram_user_id=message.from_user.id,
        collection_name=state_data.get('collection_name'),
    )
    collection = dao.get_collection(
        telegram_user_id=message.from_user.id,
        folder_id=collection.folder_id,
        collection_name=state_data.get('collection_new_name'),
    )
    if collection:
        await message.answer(
            text=(
                'The collection <b><u>{collection_name}</u></b> is already'
                ' exists in this folder!'
            ).format(
                collection_name=state_data.get('collection_new_name'),
            ),
        )
        await write_collection_name(message.answer, state)
        return

    dao.update_collection(
        collection_id=state_data.get('collection_id'),
        collection_name=state_data.get('collection_new_name'),
    )

    old_name = state_data.get('collection_name')
    new_name = state_data.get('collection_new_name')

    await state.update_data(
        collection_name=new_name,
        collection_new_name=None,
    )

    await manage_collection(
        message.answer,
        state,
        additional_text=_(
            'Collection name <u><b>{collection_name}</b></u> '
            'changed to <u><b>{new_name}</b></u>'
        ).format(
            collection_name=old_name,
            new_name=new_name,
        ),
    )
    await state_safe_clear(state)
