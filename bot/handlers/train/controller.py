from random import shuffle
from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from bot.misc.constants import (
    FIND_DEFINITION_LIMIT_OF_OPTIONS, FIND_DEFINITION_POLL_TIME,
)

import database.dao as dao
from bot.handlers.train.states import FindDefinitionStates
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.misc.support import state_safe_clear
from bot.misc.instances import bot, arq_scheduler, __

from scheduler.scheduler import FIND_DEFINITION_Q_NAME
from .callbacks import FinishTrainCallback


async def cancel_expired_time_job(state: FSMContext):
    state_data = await state.get_data()
    job_expired_time_id = state_data.get('job_expired_time_id')
    if job_expired_time_id:
        await arq_scheduler.abort_job(
            job_expired_time_id,
            FIND_DEFINITION_Q_NAME,
        )


async def guess(
    state: FSMContext,
) -> None:
    state_data = await state.get_data()
    try:
        terms = dao.get_find_definition_terms(
            collection_id=state_data.get('collection_id'),
            excluded_ids=state_data.get('used_term_ids', []),
            limit=FIND_DEFINITION_LIMIT_OF_OPTIONS,
        )
    except dao.NotEnoughTermsException:
        await finish_train(state)
        return

    correct_term = terms[0]

    used_term_ids = state_data.get('used_term_ids')
    used_term_ids.append(correct_term.id)
    await state.update_data(used_term_ids=used_term_ids)

    text = f'{correct_term.name}'
    shuffle(terms)

    correct_option_id = terms.index(correct_term)
    await state.update_data(correct_option_id=correct_option_id)
    await bot.send_poll(
        chat_id=state.key.chat_id,
        question=text,
        is_anonymous=False,
        type='quiz',
        correct_option_id=correct_option_id,
        options=(
            [
                term.description
                if len(term.description) < 100
                else f'{term.description[:97]}...'
                for term in terms
            ]
        ),
        open_period=FIND_DEFINITION_POLL_TIME,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=__('Finish train'),
                        callback_data=FinishTrainCallback().pack(),
                    ),
                ],
            ],
        ),
    )

    job_id = await arq_scheduler.enqueue_job(
        'time_was_expired',
        q_name=FIND_DEFINITION_Q_NAME,
        delay=FIND_DEFINITION_POLL_TIME,
        chat_id=state.key.chat_id,
        user_id=state.key.user_id,
    )
    await state.update_data(job_expired_time_id=job_id)


async def update_score(
    is_won: bool, state: FSMContext
):
    state_data = await state.get_data()
    if is_won:
        await state.update_data(
            wins_count=state_data.get('wins_count') + 1,
        )
    else:
        await state.update_data(
            lose_count=state_data.get('lose_count') + 1,
        )


async def finish_train(
    state: FSMContext,
    message_id: int = None,
):
    state_data = await state.get_data()
    wins_count = state_data.get('wins_count')
    lose_count = state_data.get('lose_count')
    chat_id = state_data.get('chat_id')

    accuracy = wins_count / ((wins_count + lose_count) or 1)
    func_args = dict(
        text=_(
            'Wins: {wins_count} | Loses: {lose_count}'
            '\nAccuracy: {accuracy:.1%}'
        ).format(
            wins_count=wins_count,
            lose_count=lose_count,
            accuracy=accuracy,
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Try again'),
                        callback_data=CollectionSelectCallback(
                            collection_id=state_data.get('collection_id'),
                            collection_name=state_data.get('collection_name'),
                        ).pack(),
                    ),
                ],
            ],
        ),
        parse_mode='html',
        chat_id=chat_id,
    )

    if message_id:
        await bot.edit_message_text(
            **func_args,
            message_id=message_id,
        )
    else:
        await bot.send_message(**func_args)

    await state_safe_clear(state)
    await state.set_state(FindDefinitionStates.finished_train)
