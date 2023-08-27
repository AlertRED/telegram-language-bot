from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.misc.instances import bot, dispatcher as dp, __

from .handlers.find_definition import update_score
from .callbacks import NextTryCallback, FinishTrainCallback


async def time_was_expired(ctx, chat_id: int, user_id: int):
    await bot.send_message(
        chat_id=chat_id,
        text=__('Time was expired :('),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=__('Next'),
                        callback_data=NextTryCallback().pack(),
                    ),
                    types.InlineKeyboardButton(
                        text=__('Finish train'),
                        callback_data=FinishTrainCallback().pack(),
                    ),
                ],
            ],
        ),
    )
    state = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=chat_id,
            user_id=user_id,
            bot_id=bot.id,
        ),
    )
    await state.update_data(job_expired_time_id=None)
    await update_score(False, state)
