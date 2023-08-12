from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.instances import dispatcher as dp
from bot.instances import dispatcher as dp
from bot.handlers.change_item.collection.handlers.manage import (
    manage_collection,
)
from bot.handlers.utils.handlers.browse_term import (
    CollectionIsEmptyException,
    start_browse as start_browse_term,
)
from bot.handlers.utils.calbacks import TermSelectedCallback
from ..states import ChangeTermStates
from ..callbacks import (
    ChangeTermCallback,
    ChangeTermNameCallback,
    ChangeTermDefinitionCallback,
    DeleteTermCallback,
    MoveTermCallback,
)
import database.dao as dao


@dp.callback_query(ChangeTermCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    callback_data: ChangeTermCallback,
    state: FSMContext,
) -> None:
    await state.update_data(
        collection_id=callback_data.collection_id,
        collection_name=callback_data.collection_name,
    )
    state_data = await state.get_data()
    try:
        await start_browse_term(
            callback,
            telegram_user_id=callback.from_user.id,
            collection_id=state_data['collection_id'],
        )
        await state.set_state(ChangeTermStates.manage_choose_term)
    except CollectionIsEmptyException:
        await manage_collection(
            callback.message.edit_text,
            state=state,
            additional_text=_(
                '<u><b>{collection_name}</b></u> '
                'doesn\'t have terms yet.'
            ).format(
                collection_name=state_data['collection_name'],
            ),
        )


@dp.callback_query(
    TermSelectedCallback.filter(),
    ChangeTermStates.manage_choose_term,
)
async def choose_collection(
    callback: types.CallbackQuery,
    callback_data: TermSelectedCallback,
    state: FSMContext,
) -> None:
    term = dao.get_term(callback_data.term_id)
    await state.update_data(
        term_id=callback_data.term_id,
        term_name=term.name,
        term_description=term.description,
    )

    await callback.message.edit_text(
        text=_(
            '<u><b>{name}</b></u> - {description}'
        ).format(
            name=term.name,
            description=term.description,
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Change name'),
                        callback_data=ChangeTermNameCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Change definition'),
                        callback_data=ChangeTermDefinitionCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Delete term'),
                        callback_data=DeleteTermCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Move term'),
                        callback_data=MoveTermCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeTermStates.manage_choose_option)
