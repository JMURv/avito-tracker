from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from telegram.States import SetWorker, DeleteWorker
from telegram.initializer import dp
from telegram.keyboards import keyboard_client

from data_base.crud import insert_values, delete_data, check_workers, read_data
from data_base.tracking import disable_track, register_user

from validators import url_validator
from tracking import worker_checker


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_registered = await register_user(message.from_user.id)
    if not is_registered:
        await message.answer("Привет 👋\n"
                             "Я бот, который следит за объявлениями за тебя!\n"
                             "Прочитай правила и FAQ перед использованием:"
                             " /help",
                             reply_markup=keyboard_client)
    else:
        name = message.from_user.username
        await message.answer(f"С возвращением, {name} 👋\n"
                             "Я тебя помню! Как дела?",
                             reply_markup=keyboard_client)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("FAQ:\n"
                         "1. Сколько я могу завести объявлений?\n"
                         "Ответ: Не более 5 объявлений.\n\n"
                         "2. Какая ссылка требуется для трекинга?\n"
                         "Ответ: Ссылка из поиска авито. "
                         "Можно настраивать всё, что предлагает сервис: "
                         "цену, доставку и тд.\n"
                         "Главное, что Вам нужно сделать - "
                         "установить сортировку по дате.\n\n"
                         "Предупреждение:\n"
                         "Остановка слежения может иметь задержку.",
                         reply_markup=keyboard_client)


@dp.message_handler()
async def reply_text(message: types.Message):
    if message.text == '✅ Добавить задачу':
        await set_worker(message)
    if message.text == '❌ Удалить задачу':
        await delete_worker(message)
    if message.text == '📋 Мои задачи':
        tasks = await check_workers(message.from_user.id)
        await message.answer(f"Ваши задачи: {tasks}",
                             reply_markup=keyboard_client)

    if message.text == '📡 Запустить слежение':
        await worker_checker(message, await read_data(message.from_user.id))
    if message.text == '⚠ Остановить слежение':
        await message.answer('Это может занять какое-то время..')
        await disable_track(message.from_user.id)
        await message.answer('Готово!',
                             reply_markup=keyboard_client)


@dp.message_handler(commands=['delete_worker'])
async def delete_worker(message: types.Message):
    """Start deleting a task"""
    await message.answer('Введи имя задачи')
    await DeleteWorker.delete_worker_name.set()


@dp.message_handler(state=DeleteWorker.delete_worker_name)
async def delete_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(set_worker_name=answer)
    data = await state.get_data()
    worker_name = data.get('set_worker_name')

    db_resp = await delete_data(message.from_user.id, worker_name)
    await disable_track(message.from_user.id)
    await message.answer(db_resp)
    await state.finish()


@dp.message_handler(commands=['new'], state="*")
async def set_worker(message: types.Message):
    """Start adding a task"""
    await message.answer('Введи имя задачи')
    await SetWorker.set_worker_name.set()


@dp.message_handler(state=SetWorker.set_worker_name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(set_worker_name=answer)
    await message.answer('Отправьте URL')
    await SetWorker.set_worker_url.set()


@dp.message_handler(state=SetWorker.set_worker_url)
async def get_url(message: types.Message, state: FSMContext):
    """Finish adding a task"""
    answer = message.text
    await state.update_data(set_worker_url=answer)
    data = await state.get_data()
    name = data.get('set_worker_name')
    url = data.get('set_worker_url')

    if not await url_validator(url):
        await state.finish()
        return await message.answer('Неправильный URL')

    await message.answer(f'Добавляем {name} в нашу базу..')
    await insert_values(message.from_user.id, f"'{name}'", f"'{url}'")
    await message.answer('Отлично!\n'
                         'Введите /start_track, чтобы начать слежение\n '
                         'Добавить задачу, чтобы добавить еще одно объявление')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
