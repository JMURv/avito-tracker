from loguru import logger
import asyncio
from parsing.parser import sync_avito
from telegram.initializer import bot
from telegram.keyboards import item_inline_kb
from db import DBCommands


async def form_answer(user_id: int, task: dict, name: str):
    markup = await item_inline_kb(task.get('link'))
    text = f"Обновление для {name}!\n\n" \
           f"Название: {task.get('name', '')}\n\n" \
           f"Цена: {task.get('price', '')}р\n\n" \
           f"Описание: {task.get('description', '')}\n\n"
    image = task.get('img', False)
    logger.debug(f"Image data: {image}")
    return await bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=markup,
    )


async def is_trackable(user_id: int, tasks_quantity: int) -> bool:
    db = DBCommands()
    available_workers = 1
    if await db.is_subscriber(user_id):
        available_workers = await db.worker_quantity_check(user_id)
    if tasks_quantity > available_workers:
        return False
    if await db.is_alive(user_id) == 0:
        return False
    return True


async def start_tracking():
    """
    Функция забирает активные задачи для каждого пользователя
    и формирует из них Future объект для ПОСЛЕДОВАТЕЛЬНОГО выполнения
    Это обусловлено возможностью получить бан по IP на авито или капчу
    """
    db = DBCommands()
    while True:
        active_users = await db.get_active_users()
        for user_id in list(active_users):
            tasks = await db.read_tasks(user_id)
            if not await is_trackable(user_id=user_id, tasks_quantity=len(tasks.keys())):
                continue
            for task_name, task_url in tasks.items():
                result = await asyncio.create_task(
                    asyncio.to_thread(sync_avito, task_url)
                )
                first_result = await db.read_result(user_id, task_name)
                if result is not None and result.get('name') not in first_result:
                    logger.debug("Найдено новое объявление")
                    await db.register_first_result(
                        user_id,
                        task_name,
                        result.get('name')
                    )
                    await form_answer(
                        user_id=user_id,
                        task=result,
                        name=task_name
                    )
                await asyncio.sleep(10)
