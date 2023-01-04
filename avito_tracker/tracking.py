import asyncio

from parsing.parser import async_avito
from aiogram import types
from telegram.initializer import dp
from telegram.keyboards import keyboard_short, inline_kb, keyboard_client

from data_base.DataBase import DBCommands
DB = DBCommands()


async def form_answer(user_id: int, task: dict, name: str) -> None:
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


async def start_tracking() -> None:
    while True:
        active_users = await DB.get_active_users()
        for user_id in list(active_users):
            worker = await DB.read_tasks(user_id)
            urls, tasks_names = list(worker.values()), list(worker.keys())
            tasks = list(map(
                lambda url: asyncio.create_task(async_avito(url)), urls))
            now = dict(zip(tasks_names, await asyncio.gather(*tasks)))
            for task_name in tasks_names:
                task = now.get(task_name)
                first_result = await DB.read_result(user_id, task_name)
                if task['name'] != first_result:
                    await DB.update_result(user_id, task_name, task['name'])
                    await form_answer(user_id, task, task_name)
                await asyncio.sleep(5)


async def worker_checker(message: types.Message) -> types.Message:
    user_id = message.from_user.id
    worker = await DB.read_tasks(user_id)
    tasks_names = list(worker.keys())

    avaliable_workers = 1

    if len(tasks_names) == 0:
        return await message.answer(
            'У Вас нет ни одного объявления --> '
            'Запуск невозможен',
            reply_markup=keyboard_client)

    if await DB.is_subscriber(user_id):
        avaliable_workers = await DB.worker_quantity_check(user_id)

    if len(tasks_names) > avaliable_workers:
        return await message.answer(
            f'У Вас более {avaliable_workers} объявлений! --> '
            'Запуск невозможен',
            reply_markup=keyboard_client)

    if await DB.is_exist(user_id):
        return await message.answer(
            'Ваши объявления активны',
            reply_markup=keyboard_short)
    else:
        for task in tasks_names:
            await DB.register_first_result(user_id, task, 'test_name')
        await DB.enable_track(user_id)
        return await message.answer(
                'Включаем слежение..',
                reply_markup=keyboard_short)
