from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import bot.misc.dictionaryapi as dictionaryapi
import database.dao as dao
from bot.misc import constants
from bot.handlers.utils.handlers import browse_collection
from bot.handlers.utils.calbacks import CollectionSelectCallback
from ..states import CreateTermStates
from ..callbacks import (
    AddTermCallback,
    SuggestionDefinitionChosenCallback,
)
from ..controller import write_term_name


router = Router()


@router.callback_query(AddTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse_collection.browse(callback, state)
    await state.set_state(CreateTermStates.choose_place)


@router.callback_query(
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


@router.message(CreateTermStates.write_term)
async def write_definition(
    message: types.Message,
    state: FSMContext,
) -> None:
    await state.update_data(term_name=message.text.capitalize())
    state_data = await state.get_data()

    if len(state_data.get('term_name')) > constants.MAX_TERM_NAME_LENGTH:
        await message.answer(
            text=_(
                'The term length should not be more than {max_length}!'
            ).format(
                max_length=constants.MAX_TERM_NAME_LENGTH,
            )
        )
        await write_term_name(message.answer, state)
        return

    term = dao.get_term(
        term_name=state_data.get('term_name'),
        collection_id=state_data.get('collection_id'),
    )
    if term:
        await message.answer(
            text=_(
                'The term <b><u>{term_name}</u></b> is already exists'
                ' in the collection {collection_name}!'
            ).format(
                term_name=state_data.get('term_name'),
                collection_name=state_data.get('collection_name'),
            ),
        )
        await write_term_name(message.answer, state)
        return

    suggestions = await dictionaryapi.get_definitions(state_data.get('term_name'))
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
            term_name=state_data.get('term_name'),
            text_suggestions=text_suggestions,
        ),
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
    await state.set_state(CreateTermStates.write_description)


@router.callback_query(SuggestionDefinitionChosenCallback.filter())
async def add_suggestion_definition(
    callback: types.CallbackQuery,
    callback_data: SuggestionDefinitionChosenCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    definition = \
        state_data.get('suggestions')[callback_data.suggestion_number - 1]
    await state.update_data(term_description=definition)
    await add_term(callback.message.edit_text, state, callback.from_user.id)


@router.message(CreateTermStates.write_description)
async def add_written_definition(message: types.Message, state: FSMContext):
    if len(message.text) > constants.MAX_TERM_DEFINITION_LENGTH:
        await message.answer(
            text=_(
                'The definition length should not be more than {max_length}!'
            ).format(
                max_length=constants.MAX_TERM_DEFINITION_LENGTH,
            )
        )
        await write_term_name(message.answer, state)
        return
    await state.update_data(term_description=message.text.capitalize())
    await add_term(message.answer, state, message.from_user.id)
