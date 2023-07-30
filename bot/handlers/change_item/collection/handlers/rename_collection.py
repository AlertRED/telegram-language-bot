from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from .manage import manage_collection
from ..states import ChangeCollectionStates
from ..callbacks import ChangeCollectionNameCallback
import database.dao as dao


@dp.callback_query(ChangeCollectionNameCallback.filter())
async def change_collection_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Write new name (old name {collection_name}):'
        ).format(collection_name=state_data["collection_name"]),
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
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        collection_name=message.text,
    )
    await state.update_data(
        collection_name=message.text,
    )
    await manage_collection(
        message.answer,
        state,
        additional_text=_(
            'Collection name <u><b>{collection_name}</b></u> '
            'changed to <u><b>{new_name}</b></u>'
        ).format(
            collection_name=state_data["collection_name"],
            new_name=message.text,
        ),
    )
