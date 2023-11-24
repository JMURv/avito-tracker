from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from telegram.states import AddTask, DeleteTask
from telegram.handlers.base import send_image
from telegram.initializer import dp
from telegram.keyboards import (
    main_markup,
    delete_task,
    cancel_markup,
    add_task,
    back,
    back_markup,
)
from addons.validators import url_validator
from db import DBCommands


@dp.callback_query_handler(lambda query: query.data == delete_task)
async def delete_task_handler(query: CallbackQuery) -> Message:
    await DeleteTask.name.set()
    return await query.message.answer(
        text='Введи имя задачи:',
        reply_markup=await cancel_markup()
    )


@dp.message_handler(state=DeleteTask.name)
async def delete_task_name(message: Message, state: FSMContext) -> Message:
    db = DBCommands()
    db_response = await db.delete_task(
        user_id=message.from_user.id,
        task_name=message.text
    )
    await state.finish()
    return await send_image(
        cid=message.from_user.id,
        caption=db_response,
        markup=await main_markup()
    )


@dp.callback_query_handler(lambda query: query.data == add_task)
async def add_task_handler(query: CallbackQuery) -> None:
    await query.message.answer(
        text='Введи имя задачи: ',
        reply_markup=await cancel_markup()
    )
    await AddTask.name.set()


@dp.message_handler(state=AddTask.name)
async def add_task_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_name'] = message.text
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
            text=f"Изменить название с <b>{data['task_name']}</b>?",
            reply_markup=await cancel_markup()
        )


@dp.message_handler(state=AddTask.url)
async def add_task_url(message: Message, state: FSMContext):
    db = DBCommands()
    cid = message.from_user.id
    async with state.proxy() as data:
        data['task_url'] = message.text
        name = data.get('task_name')
        url = data.get('task_url')

    if not await url_validator(url):
        await AddTask.url.set()
        return await message.answer(
            text='Неправильный URL, введите еще раз',
            reply_markup=await back_markup()
        )

    await message.answer(f'Добавляем {name} в нашу базу..')
    await db.create_task(
        user_id=cid,
        name=f"'{name}'",
        url=f"'{url}'"
    )

    await state.finish()
    return await send_image(
        cid=cid,
        caption=f"Задача {name} добавлена!",
        markup=await main_markup()
    )
