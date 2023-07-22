import database.dao as dao
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

from bot.handlers.utils.browse_collection import start_browse
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.add_item.callbacks import AddingTermCallback


router = Router()


class CreateTermStates(StatesGroup):
    choose_place = State()
    choose_term = State()
    choose_description = State()


@router.callback_query(AddingTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(CreateTermStates.choose_place)


@router.callback_query(
    CollectionSelectCallback.filter(),
    CreateTermStates.choose_place,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
    )
    await callback.message.edit_text(text='Write term')
    await state.set_state(CreateTermStates.choose_term)


@router.message(CreateTermStates.choose_term)
async def term_name_choosen(message: types.Message, state: FSMContext):
    await state.update_data(term_name=message.text.capitalize())
    user_data = await state.get_data()
    await message.answer(
        text=f'Write description for <b><u>{user_data["term_name"]}</u></b>',
        parse_mode='html',
    )
    await state.set_state(CreateTermStates.choose_description)


@router.message(CreateTermStates.choose_description)
async def term_description_choosen(message: types.Message, state: FSMContext):
    await state.update_data(term_description=message.text.capitalize())
    user_data = await state.get_data()
    dao.create_term(
        message.from_user.id,
        user_data['collection_id'],
        user_data['term_name'],
        user_data['term_description'],
    )
    await message.answer(
        text=f'Term added into {user_data["collection_name"]}\n'
        f'Term: <b><u>{user_data["term_name"]}</u></b>\n'
        f'Description: {message.text}',
        parse_mode='html',
    )
    await state.clear()
