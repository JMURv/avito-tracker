import asyncio
from aiogram import types
from parsing.parser import async_avito
from aiogram.utils.exceptions import PhotoAsInputFileRequired
from telegram.initializer import dp
from telegram.keyboards import keyboard_short, inline_kb, keyboard_client

from data_base.crud import read_data
from data_base.tracking import is_tracking_now, \
    enable_track, register_first_result, \
    check_first_result, update_result, check_if_exists

import nest_asyncio
nest_asyncio.apply()


async def start_tracking(message: types.Message, worker: dict):
    user_id = message.from_user.id
    await enable_track(user_id)
    names = list(worker.keys())
    urls = list(worker.values())
    while True:
        if await is_tracking_now(user_id) == 0:
            break
        tasks = list(map(
            lambda url: asyncio.create_task(async_avito(url)), urls))
        now = dict(zip(names, await asyncio.gather(*tasks)))
        for name in names:
            task = now.get(name)
            first_result = await check_first_result(user_id, name)
            if task['name'] != first_result:
                await update_result(user_id, name, task['name'])
                inline = await inline_kb(task['link'])
                text = f"Обновление для {name}!\n\n" \
                       f"Название: {task['name']}\n\n" \
                       f"Цена: {task['price']}р\n\n" \
                       f"Описание: {task['description']}\n\n"
                try:
                    await dp.bot.send_photo(
                        chat_id=user_id,
                        photo=f"{task['img']}",
                        caption=text,
                        reply_markup=inline
                    )
                except PhotoAsInputFileRequired:
                    await dp.bot.send_message(
                        chat_id=user_id,
                        text=f'Задача: {name}\n\n{text}',
                        reply_markup=inline
                    )
        await asyncio.sleep(10)
    return 0


@dp.message_handler(commands=['start_track'])
async def calculate_first_result(message: types.Message):
    user_id = message.from_user.id
    worker = await read_data(user_id)
    await worker_checker(message, worker)
    await message.answer('Запоминаем текущее объявление..',
                         reply_markup=keyboard_short)
    urls = list(worker.values())
    names = list(worker.keys())
    tasks = list(map(
        lambda url: asyncio.create_task(async_avito(url)), urls))
    first_results = dict(zip(names, await asyncio.gather(*tasks)))
    for task in names:
        await register_first_result(user_id, task, first_results[task]['name'])
    await message.answer(
        'Запомнили!\n'
        'Включаем слежение..')
    loop = asyncio.get_event_loop()
    new_task = loop.create_task(start_tracking(message, worker))
    loop.run_until_complete(new_task)


async def worker_checker(message: types.Message, worker):
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
    if await check_if_exists(message.from_user.id):
        await message.answer('Нашёл у Вас активные объявления, перезапуск...',
                             reply_markup=keyboard_short)
        loop = asyncio.get_event_loop()
        new_task = loop.create_task(start_tracking(message, worker))
        loop.run_until_complete(new_task)
