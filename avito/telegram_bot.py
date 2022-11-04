from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from States import SetWorker
from initializer import dp
from keyboards import keyboard_client


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
    await state.update_data(set_worker_name=answer)
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
