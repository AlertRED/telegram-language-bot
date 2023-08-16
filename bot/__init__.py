from bot.constants import LOCALES_LIST
from bot.instances import dispatcher as dp
from bot.instances import queue
from bot.commands import get_commands


async def run():
    from bot.instances import bot

    for locale in LOCALES_LIST:
        await bot.set_my_commands(
            commands=get_commands(locale),
            language_code=locale,
        )

    await queue.empty()
    await bot.delete_webhook(drop_pending_updates=True)
    from bot import handlers
    await dp.start_polling(bot)
