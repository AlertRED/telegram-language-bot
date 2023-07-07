import utils
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)
from handlers.browse_folder import (
    FolderSelectCallback,
    start_browse,
)
from handlers.add_new import AddingFolderCallback


router = Router()


class CreateFolderStates(StatesGroup):
    choose_place = State()
    choose_name = State()


@router.callback_query(AddingFolderCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(CreateFolderStates.choose_place)


@router.callback_query(
    FolderSelectCallback.filter(),
    CreateFolderStates.choose_place,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        folder_id=callback_data.folder_id,
        folder_name=callback_data.folder_name,
    )
    await callback.message.edit_text(text='Write folder name')
    await state.set_state(CreateFolderStates.choose_name)


@router.message(CreateFolderStates.choose_name)
async def create_collection(message: types.Message, state: FSMContext):
    await state.update_data(new_folder_name=message.text)
    user_data = await state.get_data()
    utils.create_folder(
        telegram_user_id=message.chat.id,
        folder_name=user_data['new_folder_name'],
        folder_id=user_data['folder_id'],
    )
    await message.answer(
        text=f'Folder <b><u>{user_data["new_folder_name"]}</u></b> '
             f'added into folder <b><u>{user_data["folder_name"]}</u></b>',
        parse_mode='html',
    )
    await state.clear()
