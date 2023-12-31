from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

import database.dao as dao
from bot.misc.constants import MIN_TERMS_COUNT_SIMPLE_TRAIN
from bot.handlers.utils.handlers.browse_collection import browse
from bot.handlers.train.handlers.menu import train_menu
from bot.handlers.utils.calbacks import CollectionSelectCallback
from bot.handlers.train.callbacks import (
    IKnowTermCallback,
    RemindTermCallback,
    SimpleTrainCallback,
)
from bot.handlers.train.states import SimpleTrainStates


router = Router()


@router.callback_query(SimpleTrainCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await browse(callback, state=state, folder_id=None, page=0)
    await state.set_state(SimpleTrainStates.choose_collection)


@router.callback_query(
    CollectionSelectCallback.filter(),
    SimpleTrainStates.choose_collection,
)
async def collection_choosen(
    callback: types.CallbackQuery,
    callback_data: CollectionSelectCallback,
    state: FSMContext,
) -> None:
    terms_count = dao.get_terms_count(
        telegram_user_id=callback.from_user.id,
        collection_id=callback_data.collection_id,
    )
    if terms_count < MIN_TERMS_COUNT_SIMPLE_TRAIN:
        await callback.message.answer(
            text=_(
                'Sorry, set must contains more than <b>{min_terms_count}</b>'
                ' terms, set <b><u>{collection_name}</u></b> has '
                '<b>{term_counts}</b> terms'
            ).format(
                min_terms_count=MIN_TERMS_COUNT_SIMPLE_TRAIN,
                collection_name=callback_data.collection_name,
                term_counts=terms_count,
            ),
        )
        await train_menu(callback.message)
    else:
        terms = dao.get_simple_train_terms(callback_data.collection_id)
        await state.update_data(
            terms=[list(term) for term in terms],
            term_index=0,
        )
        await show_term(
            callback.message,
            state,
        )
        await state.set_state(SimpleTrainStates.show_term)


@router.callback_query(IKnowTermCallback.filter())
async def know_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    if state_data.get('term_index') + 1 < len(state_data.get('terms')):
        await state.update_data(term_index=state_data.get('term_index') + 1)
        await show_term(
            callback.message,
            state,
        )
    else:
        await callback.message.edit_text(
            text=_(
                'Finished!'
            ),
        )


@router.callback_query(RemindTermCallback.filter())
async def know_term(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    term_index = state_data.get('term_index')
    terms = state_data.get('terms')
    await callback.message.edit_text(
        text=_(
            '<u><b>{name}</b></u> - {description}'
        ).format(
            name=terms[term_index][1],
            description=terms[term_index][2],
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Ok'),
                        callback_data=IKnowTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )


async def show_term(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    term_index = state_data.get('term_index')
    terms = state_data.get('terms')

    await message.edit_text(
        text=_('{name}').format(
            name=terms[term_index][1],
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Remind me'),
                        callback_data=RemindTermCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('I know'),
                        callback_data=IKnowTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )
