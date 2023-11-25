from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from telegram.callbacks import task_cb
from telegram.states import AddTask, DeleteTask
from telegram.handlers.base import send_image
from telegram.initializer import dp
from telegram.keyboards import (
    main_markup,
    delete_task,
    cancel_markup,
    add_task,
    back,
    back_markup, all_user_tasks_markup, my_tasks, accept_or_back_markup, accept, cancel,
)
from addons.validators import url_validator
from db import DBCommands


@dp.callback_query_handler(lambda query: query.data == back)
async def back_to_the_main(query: CallbackQuery):
    return await query.message.edit_reply_markup(
        reply_markup=await main_markup()
    )


@dp.callback_query_handler(lambda query: query.data == my_tasks)
async def my_tasks_handler(query: CallbackQuery):
    db = DBCommands()
    try:
        return await query.message.edit_caption(
            caption="Ваши задачи:",
            reply_markup=await all_user_tasks_markup(
                tasks_names=await db.read_user_task_names(
                    user_id=query.from_user.id
                )
            )
        )
    except MessageNotModified:
        return


@dp.callback_query_handler(task_cb.filter(action='remove'))
async def delete_task_handler(query: CallbackQuery, callback_data: dict, state: FSMContext) -> Message:
    task_name = callback_data.get("name")
    await DeleteTask.confirm.set()
    await state.update_data(task_name=task_name)
    return await query.message.edit_caption(
        caption=f"Подтвердить удаление {task_name}?",
        reply_markup=await accept_or_back_markup()
    )


@dp.callback_query_handler(lambda q: q.data in (accept, back), state=DeleteTask.confirm)
async def delete_task_confirm(query: CallbackQuery, state: FSMContext) -> Message:
    if query.data == accept:
        db = DBCommands()
        async with state.proxy() as data:
            await db.delete_task(
                user_id=query.from_user.id,
                task_name=data.get("task_name")
            )
        await state.finish()
        return await query.message.edit_caption(
            caption="",
            reply_markup=await main_markup()
        )
    else:
        await state.finish()
        return await my_tasks_handler(query)


@dp.callback_query_handler(lambda query: query.data == cancel, state=AddTask.name)
async def cancel_task_adding(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.delete()
    return await send_image(
        cid=query.from_user.id,
        caption="",
        markup=await main_markup()
    )


@dp.callback_query_handler(lambda query: query.data == add_task)
async def add_task_handler(query: CallbackQuery) -> Message:
    await AddTask.name.set()
    await query.message.answer(
        text='Введи имя задачи: ',
        reply_markup=await cancel_markup()
    )
    return await query.message.delete()


@dp.message_handler(state=AddTask.name)
async def add_task_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_task_name'] = message.text
    await AddTask.url.set()
    return await message.answer(
        'Отправьте URL',
        reply_markup=await back_markup()
    )


@dp.callback_query_handler(lambda query: query.data == back, state=AddTask.url)
async def process_task_name_back(query: CallbackQuery, state: FSMContext):
    await AddTask.name.set()
    async with state.proxy() as data:
        return await query.message.edit_text(
            text=f"Изменить название с {data['new_task_name']}?",
            reply_markup=await cancel_markup()
        )


@dp.message_handler(state=AddTask.url)
async def add_task_url(message: Message, state: FSMContext):
    db = DBCommands()
    cid = message.from_user.id
    async with state.proxy() as data:
        data['task_url'] = message.text
        name = data.get('new_task_name')
        url = data.get('task_url')

    if not await url_validator(url):
        await AddTask.url.set()
        return await message.answer(
            text='Неправильный URL, введите еще раз',
            reply_markup=await back_markup()
        )
    await db.create_task(
        user_id=cid,
        name=f"'{name}'",
        url=f"'{url}'"
    )

    await state.finish()
    return await send_image(
        cid=cid,
        caption=f"Главное меню",
        markup=await main_markup()
    )
