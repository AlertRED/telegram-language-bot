from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
import database.dao as dao
from .manage import manage_folder
from ..states import ChangeFolderStates
from ..callbacks import ChangeFolderNameCallback


@dp.callback_query(ChangeFolderNameCallback.filter())
async def change_folder_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=_(
            'Write new name (old name {folder_name}):'
        ).format(
            folder_name=state_data["folder_name"],
        ),
        parse_mode='html',
    )
    await state.set_state(ChangeFolderStates.option_change_name)


@dp.message(
    ChangeFolderStates.option_change_name,
)
async def change_folder_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_folder(
        folder_id=state_data['folder_id'],
        folder_name=message.text,
    )
    await state.update_data(
        folder_name=message.text,
    )
    await manage_folder(
        message.answer,
        state,
        additional_text=_(
            'Folder name <u><b>{folder_name}</b></u> '
            'changed to <u><b>{new_name}</b></u>\n\n'
        ).format(
            folder_name=state_data["folder_name"],
            new_name=message.text,
        ),
    )
