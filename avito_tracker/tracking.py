import asyncio
from avito_tracker.data_base.crud import read_data
from parsing.parser import async_avito
from aiogram import types
from telegram.initializer import dp
from telegram.keyboards import keyboard_short, inline_kb, keyboard_client

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
                except Exception:
                    await dp.bot.send_message(
                        chat_id=user_id,
                        text=f'Задача: {name}\n\n{text}',
                        reply_markup=inline
                    )
        await asyncio.sleep(600)
    return 0


async def calculate_first_result(message: types.Message, worker: dict):
    user_id = message.from_user.id
    urls, names = list(worker.values()), list(worker.keys())
    await message.answer('Запоминаем текущее объявление..',
                         reply_markup=keyboard_short)

    tasks = list(map(
        lambda url: asyncio.create_task(async_avito(url)), urls)
    )
    first_results = dict(zip(names, await asyncio.gather(*tasks)))
    for task in names:
        await register_first_result(user_id, task, first_results[task]['name'])
    await message.answer(
        'Запомнили!\n'
        'Включаем слежение..')
    asyncio.run(start_tracking(message, worker))


async def worker_checker(message: types.Message):
    worker = await read_data(message.from_user.id)
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
        asyncio.run(start_tracking(message, worker))
    else:
        return await calculate_first_result(message, worker)
