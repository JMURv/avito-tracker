from avito_tracker.telegram.initializer import bot
from avito_tracker.telegram.handlers import *
from avito_tracker.parsing.tracking import start_tracking
import asyncio


async def bot_start():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bot_start())
    loop.create_task(start_tracking())
    loop.run_forever()
