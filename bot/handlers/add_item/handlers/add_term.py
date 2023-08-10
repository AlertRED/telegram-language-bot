from typing import Callable
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _


import bot.utils as utils
import database.dao as dao
from bot.instances import dispatcher as dp
from bot.handlers.utils.handlers.browse_collection import start_browse
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.add_item.states import CreateTermStates
from bot.handlers.add_item.callbacks import (
    AddTermCallback,
    SuggestionDefinitionChosenCallback,
)


@dp.callback_query(AddTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(CreateTermStates.choose_place)
    await state.update_data(user_id=callback.from_user.id)


@dp.callback_query(
    CollectionSelectCallback.filter(),
    CreateTermStates.choose_place,
)
async def write_term_name_callback(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
    )
    await write_term_name(callback.message.edit_text, state)


async def write_term_name(
    foo: types.Message,
    state: FSMContext,
) -> None:
    await foo(text=_('Write term'))
    await state.set_state(CreateTermStates.choose_term)


@dp.message(CreateTermStates.choose_term)
async def term_name_choosen(message: types.Message, state: FSMContext):
    MAX_TERM_NAME_LENGTH = 128
    await state.update_data(term_name=message.text.capitalize())
    user_data = await state.get_data()

    if len(user_data['term_name']) > MAX_TERM_NAME_LENGTH:
        await message.answer(
            text=(
                'The term length should not be more than {max_length}!'
            ).format(
                max_length=MAX_TERM_NAME_LENGTH,
            )
        )
        await write_term_name(message.answer, state)
        return

    term = dao.get_term(
        term_name=user_data['term_name'],
        collection_id=user_data['collection_id'],
    )
    if term:
        await message.answer(
            text=(
                'The term <b><u>{term_name}</u></b> is already exists'
                ' in the collection {collection_name}!'
            ).format(
                term_name=user_data['term_name'],
                collection_name=user_data['collection_name'],
            ),
        )
        await write_term_name(message.answer, state)
        return

    suggestions = await utils.get_definitions(user_data['term_name'])
    await state.update_data(suggestions=suggestions)

    text_suggestions = '\n'.join(
        [
            f'{i + 1}. {suggestion}'
            for i, suggestion in enumerate(suggestions)
        ],
    )
    if text_suggestions:
        text_suggestions = _(
            'Or choose one from suggestions'
            '\n{text_suggestions}'
        ).format(text_suggestions=text_suggestions)
    else:
        text_suggestions = _('We coudn\'t find any suggestion...')

    await message.answer(
        text=_(
            'Write description for <b><u>{term_name}</u></b>'
            '\n{text_suggestions}'
        ).format(
            term_name=user_data['term_name'],
            text_suggestions=text_suggestions,
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


@dp.callback_query(SuggestionDefinitionChosenCallback.filter())
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


@dp.message(CreateTermStates.choose_description)
async def term_description_writen(message: types.Message, state: FSMContext):
    MAX_TERM_DEFINITION_LENGTH = 256
    if len(message.text) > MAX_TERM_DEFINITION_LENGTH:
        await message.answer(
            text='The definition length should not be more than {max_length}!'
            .format(max_length=MAX_TERM_DEFINITION_LENGTH)
        )
        await write_term_name(message.answer, state)
        return
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
        text=_(
            'Term added into {collection_name}\n'
            'Term: <b><u>{term_name}</u></b>\n'
            'Description: {term_description}'
        ).format(
            collection_name=user_data["collection_name"],
            term_name=user_data["term_name"],
            term_description=user_data["term_description"]
        ),
        parse_mode='html',
    )
    await state.clear()
