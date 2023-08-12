from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
import database.dao as dao
from .manage import manage_folder
from ..states import ChangeFolderStates
from ..callbacks import ChangeFolderNameCallback


@dp.callback_query(ChangeFolderNameCallback.filter())
async def write_folder_name_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await write_folder_name(callback.message, state)


async def write_folder_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.edit_text(
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
    await state.update_data(folder_new_name=message.text)
    state_data = await state.get_data()

    folder = dao.get_folder(
        telegram_user_id=message.from_user.id,
        folder_name=state_data['folder_name'],
    )
    folder = dao.get_folder(
        telegram_user_id=message.from_user.id,
        parent_folder_id=folder.parent_folder_id,
        folder_name=state_data['folder_new_name'],
    )
    if folder:
        await message.answer(
            text=(
                'The folder <b><u>{folder_name}</u></b> is already'
                ' exists in this folder!'
            ).format(
                folder_name=state_data['folder_new_name'],
            ),
        )
        await write_folder_name(message.answer, state)
        return

    dao.update_folder(
        folder_id=state_data['folder_id'],
        folder_name=message.text,
    )

    old_name = state_data['folder_name']
    new_name = state_data['folder_new_name']

    await state.update_data(
        folder_name=new_name,
        folder_new_name=None,
    )
    await manage_folder(
        message.answer,
        state,
        additional_text=_(
            'Folder name <u><b>{folder_name}</b></u> '
            'changed to <u><b>{new_name}</b></u>\n\n'
        ).format(
            folder_name=old_name,
            new_name=new_name,
        ),
    )
