from typing import Callable
from aiogram import (
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

from bot.handlers.utils.browse_collection import (
    start_browse as start_browse_collection,
)
from bot.handlers.utils.calbacks import CollectionSelectCallback
from .states import ChangeCollectionStates
from .callbacks import (
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
        text=(
            f'{additional_text}\n\n'
            f'Manage set <u><b>{state_data["collection_name"]}</b></u>'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Change name',
                        callback_data=ChangeCollectionNameCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='Move set',
                        callback_data=MoveCollectionCallback().pack(),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text='Delete set',
                        callback_data=DeleteCollectionCallback().pack(),
                    ),
                    # types.InlineKeyboardButton(
                    #     text='Change term',
                    #     callback_data=ChangeTermCallback(
                    #         collection_id=state_data.get('collection_id'),
                    #     ).pack(),
                    # ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.manage_choose_option)
