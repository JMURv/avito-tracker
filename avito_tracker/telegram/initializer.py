from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from avito_tracker.misc import BOT_ENV

bot = Bot(token=BOT_ENV.get('token'))
dp = Dispatcher(bot, storage=MemoryStorage())
