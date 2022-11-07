from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from States import SetWorker
from initializer import dp
from keyboards import keyboard_client
from time import sleep
from copy import deepcopy
from avito.avito_tracker import multi
from avito.data_base.db import insert_values, read_data, delete_data


async def calculate_first_result(user_id, message):
    worker = read_data(user_id)
    urls = list(worker.values())
    names = list(worker.keys())
    first_results = dict(zip(names, multi(urls)))
    while True:
        sleep(10)
        now = dict(zip(names, multi(urls)))
        for name in names:
            if now.get(name).get('name') != first_results.get(name).get('name'):
                first_results[name] = deepcopy(now[name])
                text = f"Обновление!\n\n" \
                       f"Название: {now[name]['name']}\n" \
                       f"Описание: {now[name]['description']}\n" \
                       f"Цена: {now[name]['price']}р\n" \
                       f"Ссылка: {now[name]['link']}\n "
            else:
                text = f'Ничего не произошло'
            await message.answer(f'Задача: {name}\n{text}')





    # first_results = {}
    # await message.answer('Запоминаем текущее объявление..\nЕсли у Вас их несколько, время загрузки вырастет')
    # for name, url in worker.items():
    #     first_results[name] = await check(worker, url)
    # await message.answer('Запомнили! Включаем слежение..')
    # while True:
    #     sleep(10)
    #     for name, url in worker.items():
    #         now = await check(worker, url)
    #         if now.get('name') != first_results.get(name).get('name'):
    #             first_results[name] = deepcopy(now)
    #             text = f"Обновление!\n\n" \
    #                    f"Название: {now['name']}\n" \
    #                    f"Описание: {now['description']}\n" \
    #                    f"Цена: {now['price']}р\n" \
    #                    f"Ссылка: {now['link']}\n "
    #             await message.answer(f'Задача: {name}\n{text}')
    #         else:
    #             text = f'Ничего не произошло'
    #             await message.answer(f'Задача: {name}\n{text}')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!\nЯ бот, который следит за объявлениями за тебя!", reply_markup=keyboard_client)


@dp.message_handler(commands=['start_track'])
async def start_tracking(message: types.Message):
    await calculate_first_result(message.from_user.id, message)


@dp.message_handler()
async def reply_text(message: types.Message):
    if message.text == 'Добавить задачу':
        await set_worker(message)
    if message.text == 'Остановить задачу':
        await message.answer('ABOBA')
    if message.text == 'Удалить задачу':
        delete_data(message.from_user.id)
        await message.answer('Успешное удаление')


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
    await message.answer(f'Добавляем {name} в нашу базу..')
    insert_values(message.from_user.id, f"'{name}'", f"'{url}'")
    await message.answer(f'Отлично!\nВведите "/start_track", чтобы начать отслеживание')
    # await start_process(message.from_user.id, message)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
