from random import shuffle

from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.utils.browse_collection import start_browse
from bot.handlers.train.callbacks import (
    FindDefinitionCallback,
    FinishGameCallback,
    TryGuessCallback,
)
import database.dao as dao


router = Router()


class FindDefinitionStates(StatesGroup):
    choose_collection = State()
    try_guess = State()


@router.callback_query(FindDefinitionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse(callback, folder_id=None, page=0)
    await state.set_state(FindDefinitionStates.choose_collection)


@router.callback_query(
    CollectionSelectCallback.filter(),
    FindDefinitionStates.choose_collection,
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
    await guess(
        None,
        callback_data.collection_id,
        callback.message,
    )
    await state.set_state(FindDefinitionStates.try_guess)


@router.callback_query(
    TryGuessCallback.filter(),
    FindDefinitionStates.try_guess,
)
async def guess_again(
    callback: types.CallbackQuery,
    callback_data: TryGuessCallback,
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    if (callback_data.previous_result is not None):
        if (callback_data.previous_result):
            results = 'You won!'
            await state.update_data(
                win_count=state_data.get('win_count', 0) + 1,
            )
        else:
            await state.update_data(
                lose_count=state_data.get('lose_count', 0) + 1,
            )
            term = dao.get_term(callback_data.right_term_id)
            results = (
                f'Wrong :(\n'
                f'<u><b>{term.name}</b></u>'
                f' - {term.description}'
            )
    else:
        results = ''

    state_data = await state.get_data()
    await guess(
        results,
        state_data['collection_id'],
        callback.message,
        state_data.get('win_count', 0),
        state_data.get('lose_count', 0),
    )
    await state.set_state(FindDefinitionStates.try_guess)


async def guess(
    prev_results: str,
    collection_id: int,
    message: types.Message,
    win_count: int = 0,
    lose_count: int = 0,
) -> None:
    terms = dao.get_find_definition_terms(
        collection_id=collection_id,
    )
    first_term_id: int = terms[0].id
    text = (
        f'{prev_results or ""}\n\n<u><b>{terms[0].name}</b></u> is ...\n'
    )
    rows = []
    options = []

    shuffle(terms)
    for i, term in enumerate(terms):
        text += f'\n{i + 1}. {term.description}'
        options.append(
            types.InlineKeyboardButton(
                text=f'{i + 1}',
                callback_data=TryGuessCallback(
                    term_name=term.name,
                    previous_result=term.id == first_term_id,
                    right_term_id=(
                        None
                        if term.id == first_term_id
                        else term.id
                    ),
                ).pack(),
            ),
        )
    rows.append(options)
    rows.append(
        [
            types.InlineKeyboardButton(
                text='End game',
                callback_data=FinishGameCallback(
                    win_count=win_count,
                    lose_count=lose_count,
                ).pack(),
            ),
        ],
    )

    await message.edit_text(
        text=text,
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )


@router.callback_query(
    FinishGameCallback.filter(),
)
async def finish_game(
    callback: types.CallbackQuery,
    callback_data: FinishGameCallback,
    state: FSMContext,
) -> None:
    total_games = (callback_data.win_count + callback_data.lose_count) or 1
    accuracy = callback_data.win_count / total_games
    await callback.message.edit_text(
        text=(
            f'Wins: {callback_data.win_count}'
            f' | Loses: {callback_data.lose_count}'
            f'\n Accuracy: {accuracy:.1%}'
        ),
    )
    await state.clear()
