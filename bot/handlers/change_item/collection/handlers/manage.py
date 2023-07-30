from typing import Callable
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from bot.handlers.change_item.term.callbacks import ChangeTermCallback
from bot.handlers.utils.browse_collection import (
    start_browse as start_browse_collection,
)
from bot.handlers.utils.calbacks import CollectionSelectCallback
from ..states import ChangeCollectionStates
from ..callbacks import (
    ChangeCollectionCallback,
    ChangeCollectionNameCallback,
    DeleteCollectionCallback,
    MoveCollectionCallback,
)


router = Router()


@router.callback_query(ChangeCollectionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse_collection(callback)
    await state.set_state(ChangeCollectionStates.manage_choose_place)


@router.callback_query(
    CollectionSelectCallback.filter(),
    ChangeCollectionStates.manage_choose_place,
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
    await manage_collection(
        callback.message.edit_text,
        state,
    )


async def manage_collection(
    send_message_foo: Callable,
    state: FSMContext,
    additional_text: str = '',
) -> None:
    state_data = await state.get_data()
    await send_message_foo(
        text=_(
            '{additional_text}\n\n'
            'Manage set <u><b>{collection_name}</b></u>'
        ).format(
            additional_text=additional_text,
            collection_name=state_data["collection_name"],
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=_('Change name'),
                        callback_data=ChangeCollectionNameCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Move set'),
                        callback_data=MoveCollectionCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=_('Delete set'),
                        callback_data=DeleteCollectionCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=_('Change term'),
                        callback_data=ChangeTermCallback(
                            collection_id=state_data.get('collection_id'),
                            collection_name=state_data.get('collection_name'),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.manage_choose_option)
