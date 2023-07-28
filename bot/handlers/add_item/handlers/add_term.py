from typing import Callable

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
from bot.handlers.add_item.callbacks import (
    AddingTermCallback,
    SuggestionDefinitionChosenCallback,
)
import bot.utils as utils
import database.dao as dao


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
    await state.update_data(user_id=callback.from_user.id)


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

    suggestions = await utils.get_definitions(user_data['term_name'])
    await state.update_data(suggestions=suggestions)

    text_suggestions = '\n'.join(
        [f'{i + 1}. {suggestion}' for i, suggestion in enumerate(suggestions)],
    )
    if text_suggestions:
        text_suggestions = (
            f'Or choose one from suggestions'
            f'\n{text_suggestions}'
        )
    else:
        text_suggestions = 'We coudn\'t find any suggestion...'

    await message.answer(
        text=(
            f'Write description for <b><u>{user_data["term_name"]}</u></b>'
            f'\n{text_suggestions}'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=str(i),
                        callback_data=SuggestionDefinitionChosenCallback(
                            suggestion_number=i,
                        ).pack(),
                    ) for i in range(1, len(suggestions) + 1)
                ],
            ],
        ),
    )
    await state.set_state(CreateTermStates.choose_description)


@router.callback_query(SuggestionDefinitionChosenCallback.filter())
async def term_definition_chosen(
    callback: types.CallbackQuery,
    callback_data: SuggestionDefinitionChosenCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    definition = \
        state_data.get('suggestions')[callback_data.suggestion_number - 1]
    await state.update_data(term_description=definition)
    await add_term(callback.message.edit_text, state)


@router.message(CreateTermStates.choose_description)
async def term_description_writen(message: types.Message, state: FSMContext):
    await state.update_data(term_description=message.text.capitalize())
    await add_term(message.answer, state)


async def add_term(foo_answer: Callable, state: FSMContext):
    user_data = await state.get_data()
    dao.create_term(
        user_data['user_id'],
        user_data['collection_id'],
        user_data['term_name'],
        user_data['term_description'],
    )
    await foo_answer(
        text=f'Term added into {user_data["collection_name"]}\n'
        f'Term: <b><u>{user_data["term_name"]}</u></b>\n'
        f'Description: {user_data["term_description"]}',
        parse_mode='html',
    )
    await state.clear()
