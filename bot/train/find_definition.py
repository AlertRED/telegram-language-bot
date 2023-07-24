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

from bot.utils.calbacks import CollectionSelectCallback
from bot.utils.browse_collection import start_browse
from bot.train.callbacks import (
    FindDefinitionCallback,
    FinishGameCallback,
    TryGuessCallback,
)
import database.dao as dao


router = Router()


class FindDefinitionStates(StatesGroup):
    choose_collection = State()
    try_guess = State()
    finished_train = State()


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
@router.callback_query(
    CollectionSelectCallback.filter(),
    FindDefinitionStates.finished_train,
)
async def start_train(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
        wins_count=0,
        lose_count=0,
        used_term_ids=[],
    )
    await guess(
        message=callback.message,
        state=state,
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

    used_term_ids = state_data.get('used_term_ids')
    used_term_ids.append(callback_data.right_term_id)
    await state.update_data(used_term_ids=used_term_ids)
    if (callback_data.previous_result):
        results = 'You won!🎉'
        await state.update_data(
            wins_count=state_data.get('wins_count') + 1,
        )
    else:
        await state.update_data(
            lose_count=state_data.get('lose_count') + 1,
        )
        term = dao.get_term(callback_data.right_term_id)
        results = (
            f'Wrong :(\n'
            f'<u><b>{term.name}</b></u>'
            f' - {term.description}'
        )

    await state.update_data(prev_results=results)
    await guess(
        callback.message,
        state=state,
    )


async def guess(
    message: types.Message,
    state: FSMContext,
) -> None:
    LIMIT_OF_OPTIONS: int = 4
    state_data = await state.get_data()
    try:
        terms = dao.get_find_definition_terms(
            collection_id=state_data.get('collection_id'),
            excluded_ids=state_data.get('used_term_ids', []),
            limit=LIMIT_OF_OPTIONS,
        )
    except dao.NotEnoughTermsException:
        await _finish_game(message, state)
        return

    first_term_id: int = terms[0].id
    prev_results = state_data.get('prev_results', '')
    if prev_results:
        prev_results = f'{prev_results}\n\n'
    text = (
        f'{prev_results}'
        f'<u><b>{terms[0].name}</b></u> is:\n'
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
                    previous_result=term.id == first_term_id,
                    right_term_id=first_term_id,
                ).pack(),
            ),
        )
    rows.append(options)
    rows.append(
        [
            types.InlineKeyboardButton(
                text='End game',
                callback_data=FinishGameCallback().pack(),
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
    await state.set_state(FindDefinitionStates.try_guess)


@router.callback_query(FinishGameCallback.filter())
async def finish_game(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await _finish_game(callback.message, state, is_ended_by_user=False)


async def _finish_game(
    message: types.Message,
    state: FSMContext,
    is_ended_by_user: bool = True,
):
    state_data = await state.get_data()
    wins_count = state_data.get('wins_count')
    lose_count = state_data.get('lose_count')

    accuracy = wins_count / ((wins_count + lose_count) or 1)

    prev_results = state_data.get('prev_results')
    if prev_results:
        prev_results = f'{prev_results}\n\n'

    await message.edit_text(
        text=(
            f'{prev_results if is_ended_by_user else ""}'
            f'Wins: {wins_count} | Loses: {lose_count}'
            f'\nAccuracy: {accuracy:.1%}'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Try again',
                        callback_data=CollectionSelectCallback(
                            collection_id=state_data.get('collection_id'),
                            collection_name=state_data.get('collection_name'),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.clear()
    await state.set_state(FindDefinitionStates.finished_train)
