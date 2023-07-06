import utils
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

from handlers.callbacks import (
    AddTermCallback,
)
from handlers import states
from handlers.browse_collection import folder_chosen


router = Router()


@router.callback_query(AddTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_data(
        {'folder_id': None, 'page': 0, 'result_foo': collection_choosen},
    )
    await folder_chosen(callback, state)


async def collection_choosen(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.edit_text(text='Write term:')
    await state.set_state(states.AddNewTermState.add_term)


@router.message(states.AddNewTermState.add_term)
async def term_name_choosen(message: types.Message, state: FSMContext):
    await state.update_data(term_name=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f'Write description for <b><u>{user_data["term_name"]}</u></b>:',
        parse_mode='html',
    )
    await state.set_state(states.AddNewTermState.add_description)


@router.message(states.AddNewTermState.add_description)
async def term_description_choosen(message: types.Message, state: FSMContext):
    await state.update_data(term_description=message.text)
    user_data = await state.get_data()
    utils.create_term(
        message.chat.id,
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
