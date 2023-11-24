from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from telegram.initializer import dp
from db import DBCommands
from telegram.keyboards import (
    main_markup,
    start_all_tasks,
    active_tracking_markup,
    stop_all_tasks
)


@dp.callback_query_handler(lambda query: query.data == start_all_tasks)
async def start_tracking_handler(query: CallbackQuery) -> Message:
    db = DBCommands()
    uid = query.from_user.id
    worker = await db.read_tasks(
        user_id=uid
    )
    tasks_names = list(worker.keys())

    available_workers = 1

    if len(tasks_names) == 0:
        return await query.message.edit_caption(
            caption='У Вас нет ни одного объявления!',
            reply_markup=await main_markup()
        )

    # Если подписчик - обновляем доступные объявления
    if await db.is_subscriber(uid):
        available_workers = await db.worker_quantity_check(
            user_id=uid
        )

    if len(tasks_names) > available_workers:
        return await query.message.edit_caption(
            caption=f'У Вас более {available_workers} объявлений!',
            reply_markup=await main_markup()
        )

    # Проверяем запущен ли уже трекинг
    if await db.is_exist(user_id=uid):
        return await query.message.edit_caption(
            caption='Ваши объявления активны!',
            reply_markup=await active_tracking_markup()
        )
    else:
        for task_name in tasks_names:
            await db.register_first_result(
                user_id=uid,
                task_name=task_name,
                first_result_name='test_name'
            )
        await db.enable_track(uid)
        return await query.message.edit_caption(
            caption='Слежение включено!',
            reply_markup=await active_tracking_markup()
        )


@dp.callback_query_handler(lambda query: query.data == stop_all_tasks)
async def stop_tracking_handler(query: CallbackQuery) -> Message:
    db = DBCommands()
    await db.disable_track(query.from_user.id)
    await query.answer(text='Трекинг остановлен')
    with open('./data/avito_logo.png', 'rb') as photo:
        await query.message.edit_caption(caption='')
        return await query.message.edit_media(
            media=InputMediaPhoto(media=photo),
            reply_markup=await main_markup()
        )
