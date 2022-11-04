import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from States import SetWorker

TOKEN = '5679447524:AAGZiFO08CAvliBV9J3foebr4W1TDBxOKKY'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


b1 = KeyboardButton('Добавить задачу')
b2 = KeyboardButton('Удалить задачу')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.row(b1, b2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=keyboard_client)


@dp.message_handler(commands=['set_new'])
async def set_worker(message: types.Message):
    await message.answer('Введи имя задачи')
    await SetWorker.set_worker_name.set()


@dp.message_handler(state=SetWorker.set_worker_name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(set_worker_name=answer)  # Имя задачи в worker_name
    await message.answer(f'Отправьте правильный URL для задачи {answer}')
    await SetWorker.set_worker_url.set()


@dp.message_handler(state=SetWorker.set_worker_url)
async def get_url(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(set_worker_url=answer)

    data = await state.get_data()
    name = data.get('set_worker_name')
    url = data.get('set_worker_url')
    await message.answer(f'Имя: {name}\nURL: {url}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
