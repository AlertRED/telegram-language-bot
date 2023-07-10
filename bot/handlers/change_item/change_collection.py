from typing import Callable
import database.dao as dao
from aiogram import (
    Router,
    types,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State,
)

from bot.handlers.utils.browse_folder import (
    start_browse as start_browse_folder,
)
from bot.handlers.utils.browse_collection import (
    start_browse as start_browse_collection,
)
from bot.handlers.utils.calbacks import (
    FolderSelectCallback,
    CollectionSelectCallback,
)
from bot.handlers.change_item.callbacks import (
    ChangeCollectionCallback,
    ChangeCollectionNameCallback,
    DeleteCollectionCallback,
    MoveCollectionCallback,
)


router = Router()


class MoveCollectionsStates(StatesGroup):
    choose_folder = State()
    agree = State()


class ChangeCollectionStates(StatesGroup):
    choose_place = State()
    change_name = State()


@router.callback_query(ChangeCollectionCallback.filter())
async def choose_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await start_browse_collection(callback)
    await state.set_state(ChangeCollectionStates.choose_place)


@router.callback_query(
    CollectionSelectCallback.filter(),
    ChangeCollectionStates.choose_place,
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
            f'{additional_text}'
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
                ],
                [
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
                ],
            ],
        ),
    )


### Move collection

@router.callback_query(
    MoveCollectionCallback.filter(F.sure == True),
)
async def move_collection_true(
    callback: types.CallbackQuery,
    callback_data: MoveCollectionCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        folder_id=callback_data.folder_id,
    )
    await manage_collection(
        callback.message.edit_text,
        state,
        additional_text=(
            f'{state_data["collection_name"]} was moved to '
            f'{callback_data.folder_name}\n\n'
        ),
    )


@router.callback_query(
    MoveCollectionCallback.filter(F.sure == False),
)
async def move_collection_false(
    callback: types.CallbackQuery,
    callback_data: MoveCollectionCallback,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(MoveCollectionCallback.filter())
async def move_collection_browse(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await start_browse_folder(callback)
    await state.set_state(MoveCollectionsStates.choose_folder)


@router.callback_query(
    FolderSelectCallback.filter(),
    MoveCollectionsStates.choose_folder,
)
async def move_collection_sure(
    callback: types.CallbackQuery,
    callback_data: FolderSelectCallback,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure wanna move '
            f'<u><b>{state_data["collection_name"]}</b></u>'
            f' into <u><b>{callback_data.folder_name}</b></u>?'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=MoveCollectionCallback(
                            sure=True,
                            folder_id=callback_data.folder_id,
                            folder_name=callback_data.folder_name,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=MoveCollectionCallback(sure=False).pack(),
                    ),
                ],
            ],
        ),
    )


### Delete collection


@router.callback_query(DeleteCollectionCallback.filter(F.sure == False))
async def delete_collection(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await manage_collection(
        callback.message.edit_text,
        state,
    )


@router.callback_query(DeleteCollectionCallback.filter(F.sure == True))
async def delete_collection_false(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.delete_collection(state_data['collection_id'])
    await callback.message.answer(
        text=(
            f'Collection <u><b>{state_data["collection_name"]}</b></u>'
            f' deleted succesfully!\n\n'
        ),
        parse_mode='html',
    )


@router.callback_query(DeleteCollectionCallback.filter())
async def delete_collection_true(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=(
            f'Are you sure you wanna delete '
            f'<u><b>{state_data["collection_name"]}</b></u>?\n'
            f'All terms inside will be deleted too!'
        ),
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Yes',
                        callback_data=DeleteCollectionCallback(
                            sure=True,
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='No',
                        callback_data=DeleteCollectionCallback(
                            sure=False,
                        ).pack(),
                    ),
                ],
            ],
        ),
    )
    await state.set_state(ChangeCollectionStates.change_name)


### Change collection name

@router.callback_query(ChangeCollectionNameCallback.filter())
async def change_collection_name(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.message.edit_text(
        text=f'Write new name (old name {state_data["collection_name"]}):',
        parse_mode='html',
    )
    await state.set_state(ChangeCollectionStates.change_name)


@router.message(
    ChangeCollectionStates.change_name,
)
async def change_collection_name(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    dao.update_collection(
        collection_id=state_data['collection_id'],
        collection_name=message.text,
    )
    await state.update_data(
        collection_name=message.text,
    )
    await manage_collection(
        message.answer,
        state,
        additional_text=(
            f'Collection name <u><b>{state_data["collection_name"]}</b></u> '
            f'changed to <u><b>{message.text}</b></u>\n\n'
        ),
    )

###
