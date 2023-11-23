from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageNotModified
from telegram import States
from telegram.initializer import dp, bot
from telegram.keyboards import (
    main_markup,
    delete_task,
    cancel_markup,
    cancel,
    add_task,
    back,
    back_markup,
    my_tasks,
    buy_subscription,
    start_all_tasks,
    active_tracking_markup,
    stop_all_tasks
)
from telegram.payment import calculate_price
from addons.validators import url_validator, payment_validator
from data_base import DBCommands


DB = DBCommands()


async def send_image(cid, caption: str, markup: types.InlineKeyboardMarkup):
    with open('./data/avito_logo.png', 'rb') as photo:
        return await bot.send_photo(
            chat_id=cid,
            photo=photo,
            caption=caption,
            reply_markup=markup
        )


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_registered = await DB.create_user(message.from_user.id)
    hello_text = "Привет 👋\n" \
                 "Я бот, который следит за объявлениями за тебя!\n" \
                 "Прочитай правила и FAQ перед использованием: " \
                 "/help"
    if is_registered:
        hello_text = f"С возвращением, {message.from_user.username} 👋\n"
    with open('./data/avito_logo.png', 'rb') as photo:
        return await message.answer_photo(
            photo=photo,
            caption=hello_text,
            reply_markup=await main_markup()
        )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(
        "FAQ:\n"
        "1. Сколько я могу завести объявлений?\n"
        "Ответ: Не более 1 объявления для бесплатного аккаунта.\n\n"
        "2. Какая ссылка требуется для трекинга?\n"
        "Ответ: Ссылка из поиска авито. "
        "Выбирайте отображение списком, не плит!"
        "Можно настраивать всё, что предлагает сервис: "
        "цену, доставку и тд.\n"
        "Главное, что Вам нужно сделать - "
        "установить сортировку по дате, "
        "иначе бот будет работать неправильно.\n\n",
        reply_markup=await main_markup()
    )


@dp.callback_query_handler(lambda query: query.data == cancel, state='*')
async def cancel_handler(query: types.CallbackQuery | types.Message, state: FSMContext):
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == my_tasks)
async def my_tasks_handler(query: types.CallbackQuery):
    tasks = await DB.read_user_task(query.from_user.id)
    try:
        return await query.message.edit_caption(
            caption=f"Ваши задачи: \n{tasks}",
            reply_markup=await main_markup()
        )
    except MessageNotModified:
        return await query.message.edit_reply_markup(
            reply_markup=await main_markup()
        )


@dp.callback_query_handler(lambda query: query.data == start_all_tasks)
async def start_tracking_handler(query: types.CallbackQuery) -> types.Message:
    uid = query.from_user.id
    worker = await DB.read_tasks(
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
    if await DB.is_subscriber(uid):
        available_workers = await DB.worker_quantity_check(
            user_id=uid
        )

    if len(tasks_names) > available_workers:
        return await query.message.edit_caption(
            caption=f'У Вас более {available_workers} объявлений!',
            reply_markup=await main_markup()
        )

    # Проверяем запущен ли уже трекинг
    if await DB.is_exist(user_id=uid):
        return await query.message.edit_caption(
            caption='Ваши объявления активны!',
            reply_markup=await active_tracking_markup()
        )
    else:
        for task_name in tasks_names:
            await DB.register_first_result(
                user_id=uid,
                task_name=task_name,
                first_result_name='test_name'
            )
        await DB.enable_track(uid)
        return await query.message.edit_caption(
            caption='Слежение включено!',
            reply_markup=await active_tracking_markup()
        )


@dp.callback_query_handler(lambda query: query.data == stop_all_tasks)
async def stop_tracking_handler(query: types.CallbackQuery) -> types.Message:
    await DB.disable_track(query.from_user.id)
    await query.answer(text='Трекинг остановлен')
    with open('./data/avito_logo.png', 'rb') as photo:
        await query.message.edit_caption(caption='')
        return await query.message.edit_media(
            media=InputMediaPhoto(media=photo),
            reply_markup=await main_markup()
        )


@dp.callback_query_handler(lambda query: query.data == buy_subscription)
async def buy_subscription_handler(query: types.CallbackQuery) -> types.Message:
    if await DB.is_subscriber(query.from_user.id):
        return await query.message.answer(
            text='У вас уже есть подписка!',
            reply_markup=await main_markup()
        )
    await States.BuySubscription.how_long.set()
    return await query.message.answer(
        text='Сколько дней подписки хотите?\n'
        'Напишите количество.',
        reply_markup=await cancel_markup()
    )


@dp.message_handler(state=States.BuySubscription.how_long)
async def get_time(message: types.Message, state: FSMContext) -> types.Message:
    async with state.proxy() as data:
        data['how_long'] = message.text
    await States.BuySubscription.how_many.set()
    return await message.answer(
        text='Как много объявлений хотите отслежвать?',
        reply_markup=await back_markup()
    )


@dp.message_handler(state=States.BuySubscription.how_many)
async def get_quantity(message: types.Message, state: FSMContext) -> None:
    uid = message.from_user.id
    answer = message.text
    await state.update_data(how_many=answer)
    data = await state.get_data()

    worker_quantity, days = data.get('how_many'), data.get('how_long')
    if not await payment_validator(worker_quantity, days):
        await state.finish()
        await message.answer(
            'Неправильные данные',
            reply_markup=await main_markup()
        )

    await state.finish()
    subscription_data = {
        'worker_quantity': worker_quantity,
        'days': days,
        'amount': await calculate_price(worker_quantity, days)
    }


@dp.callback_query_handler(lambda query: query.data == delete_task)
async def delete_task_handler(query: types.CallbackQuery) -> types.Message:
    await States.DeleteTask.name.set()
    return await query.message.answer(
        text='Введи имя задачи:',
        reply_markup=await cancel_markup()
    )


@dp.message_handler(state=States.DeleteTask.name)
async def delete_task_name(message: types.Message, state: FSMContext) -> types.Message:
    db_response = await DB.delete_task(
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
async def add_task_handler(query: types.CallbackQuery) -> None:
    await query.message.answer(
        text='Введи имя задачи: ',
        reply_markup=await cancel_markup()
    )
    await States.AddTask.name.set()


@dp.message_handler(state=States.AddTask.name)
async def add_task_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_name'] = message.text
    await States.AddTask.url.set()
    return await message.answer(
        'Отправьте URL',
        reply_markup=await back_markup()
    )


@dp.callback_query_handler(lambda query: query.data == back, state=States.AddTask.url)
async def process_task_name_back(query: types.CallbackQuery, state: FSMContext):
    await States.AddTask.name.set()
    async with state.proxy() as data:
        return await query.message.edit_text(
            text=f"Изменить название с <b>{data['task_name']}</b>?",
            reply_markup=await cancel_markup()
        )


@dp.message_handler(state=States.AddTask.url)
async def add_task_url(message: types.Message, state: FSMContext):
    cid = message.from_user.id
    async with state.proxy() as data:
        data['task_url'] = message.text
        name = data.get('task_name')
        url = data.get('task_url')

    if not await url_validator(url):
        await States.AddTask.url.set()
        return await message.answer(
            text='Неправильный URL, введите еще раз',
            reply_markup=await back_markup()
        )

    await message.answer(f'Добавляем {name} в нашу базу..')
    await DB.create_task(
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


async def bot_start():
    await dp.start_polling(bot)
