from aiogram import (
    Router,
    filters,
    types,
)
from aiogram.fsm.context import FSMContext

from handlers.callbacks import (
    AddTermCallback,
)


router = Router()


@router.message(
    filters.Command('add_new'),
)
async def add_new(
    message: types.Message,
) -> None:
    rows = [
        [
            types.InlineKeyboardButton(
                text='Add term',
                callback_data=AddTermCallback().pack(),
            ),
        ],
        # [types.InlineKeyboardButton(text='Add set')],
        # [types.InlineKeyboardButton(text='Add folder')],
        # [types.InlineKeyboardButton(text='Go back')],
    ]
    await message.answer(
        text='What do you wonna add:',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=rows,
        ),
    )





# @router.message(states.AddNewTermState.add_description)
# async def add_new_collection(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     utils.create_collection(message.chat.id, user_data["term_name"])
#     await message.answer(
#         text=f'Term added\n'
#         f'Term: <b><u>{user_data["term_name"]}</u></b>\n'
#         f'Description: {message.text}',
#         parse_mode='html',
#     )
#     await state.clear()
