import asyncio
from copy import deepcopy
from urllib.parse import urlparse

from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from telegram.States import SetWorker, DeleteWorker
from telegram.initializer import dp
from telegram.keyboards import keyboard_client, keyboard_short

from parsing.parser import async_avito
from data_base.crud import insert_values, read_data, delete_data
from data_base.tracking import is_tracking_now, disable_track, register_user, enable_track


async def tracking(message, worker, first_results):
    user_id = message.from_user.id
    enable_track(user_id)
    names = list(worker.keys())
    urls = list(worker.values())
    while True:
        if is_tracking_now(user_id) == 0:
            break
        tasks = list(map(
            lambda url: asyncio.create_task(async_avito(url)), urls))
        now = dict(zip(names, await asyncio.gather(*tasks)))
        for name in names:
            task = now.get(name)
            if task['name'] != first_results.get(name)['name']:
                first_results[name] = deepcopy(now[name])
                text = f"Обновление!\n\n" \
                       f"Название: {task['name']}\n\n" \
                       f"Цена: {task['price']}р\n\n" \
                       f"Описание: {task['description']}\n\n" \
                       f"Ссылка: {task['link']}\n\n"
                await message.answer(f'Задача: {name}\n\n{text}')
        await asyncio.sleep(600)
    await message.answer(
        'Сворачиваем слежение..',
        reply_markup=keyboard_client)


async def worker_validator(message, worker):
    if len(worker.keys()) == 0:
        return await message.answer(
            'У Вас нет ни одного объявления --> '
            'Запуск невозможен',
            reply_markup=keyboard_client)
    if len(worker.keys()) > 5:
        return await message.answer(
            'У Вас более 5 объявлений! --> '
            'Запуск невозможен',
            reply_markup=keyboard_client)


async def calculate_first_result(user_id, message):
    worker = read_data(user_id)
    await worker_validator(message, worker)
    await message.answer('Запоминаем текущее объявление..',
                         reply_markup=keyboard_short)
    urls = list(worker.values())
    names = list(worker.keys())
    tasks = list(map(
        lambda url: asyncio.create_task(async_avito(url)), urls))
    first_results = dict(zip(names, await asyncio.gather(*tasks)))
    await message.answer(
        'Запомнили!\n'
        'Включаем слежение..')
    await tracking(message, worker, first_results)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_registered = register_user(message.from_user.id)
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


@dp.message_handler(commands=['start_track'])
async def start_tracking(message: types.Message):
    await calculate_first_result(message.from_user.id, message)


@dp.message_handler()
async def reply_text(message: types.Message):
    if message.text == '✅ Добавить задачу':
        await set_worker(message)
    if message.text == '❌ Удалить задачу':
        await delete_worker(message)

    if message.text == '📡 Запустить слежение':
        await start_tracking(message)
    if message.text == '⚠ Остановить слежение':
        await message.answer('Это может занять какое-то время')
        disable_track(message.from_user.id)


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

    db_resp = delete_data(message.from_user.id, worker_name)
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

    if urlparse(url).netloc != 'www.avito.ru':
        await state.finish()
        return await message.answer('Неправильный URL')

    await message.answer(f'Добавляем {name} в нашу базу..')
    insert_values(message.from_user.id, f"'{name}'", f"'{url}'")
    await message.answer('Отлично!\n'
                         'Введите /start_track, чтобы начать слежение\n '
                         'Добавить задачу, чтобы добавить еще одно объявление')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
