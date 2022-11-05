from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from States import SetWorker
from initializer import dp
from keyboards import keyboard_client
from avito_tracker import get_avito
from time import sleep


def five_min_call(url):
    while True:
        sleep(10)
        return get_avito(url)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот, который следит за объявлениями за тебя!", reply_markup=keyboard_client)


@dp.message_handler()
async def reply_text(message: types.Message):
    if message.text == 'Добавить задачу':
        await set_worker(message)
    else:
        await message.reply("АБОБА", reply_markup=keyboard_client)


@dp.message_handler(commands=['set_new'])
async def set_worker(message: types.Message):
    """Start adding a task"""
    await message.answer('Введи имя задачи')
    await SetWorker.set_worker_name.set()


@dp.message_handler(state=SetWorker.set_worker_name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(set_worker_name=answer)
    await message.answer(f'Отправьте URL')
    await SetWorker.set_worker_url.set()


@dp.message_handler(state=SetWorker.set_worker_url)
async def get_url(message: types.Message, state: FSMContext):
    """Finish adding a task"""
    answer = message.text
    await state.update_data(set_worker_url=answer)

    data = await state.get_data()
    name = data.get('set_worker_name')
    url = data.get('set_worker_url')
    await message.answer(f'Отлично!\nНачинаю следить за {name}')

    await message.answer(five_min_call(url))  # Функция вызывающая авито каждые 5 минут
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
