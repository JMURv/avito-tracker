from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = '5679447524:AAGZiFO08CAvliBV9J3foebr4W1TDBxOKKY'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
