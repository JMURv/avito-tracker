import os

from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from telegram.States import SetWorker, DeleteWorker, BuySubscription
from telegram.initializer import dp
from telegram.keyboards import keyboard_client, keyboard_workers

from data_base.crud import insert_values, delete_data, check_workers
from data_base.tracking import disable_track, register_user

from avito_tracker.payment import form_bill, calculate_price
from validators import url_validator, payment_validator
from tracking import worker_checker, start_tracking


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    is_registered = await register_user(message.from_user.id)
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
async def send_help(message: types.Message) -> None:
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


@dp.message_handler()
async def reply_text(message: types.Message) -> None:
    if message.text == os.getenv('start_password'):
        await start_tracking()
    if message.text in ('✅ Добавить задачу', '/add'):
        await set_worker(message)
    if message.text in ('❌ Удалить задачу', '/delete'):
        await delete_worker(message)
    if message.text == '📋 Мои задачи':
        tasks = await check_workers(message.from_user.id)
        await message.answer(f"Ваши задачи: {tasks}",
                             reply_markup=keyboard_client)
    if message.text in ('📡 Запустить слежение', '/start_track'):
        await worker_checker(message)
    if message.text == '⚠ Остановить слежение':
        await message.answer('Это может занять какое-то время..')
        await disable_track(message.from_user.id)
        await message.answer('Готово!',
                             reply_markup=keyboard_client)
    if message.text == 'Купить подписку':
        await buy_subscription(message)


@dp.message_handler(commands=['buy'])
async def buy_subscription(message: types.Message) -> None:
    await message.answer(
        'Сколько дней подписки хотите?\n'
        'Напишите количество.'
    )
    await BuySubscription.how_long.set()


@dp.message_handler(state=BuySubscription.how_long)
async def get_time(message: types.Message, state: FSMContext) -> None:
    answer = message.text
    await state.update_data(how_long=answer)
    await message.answer(
        'Как много объявлений хотите отслежвать?',
        reply_markup=keyboard_workers
    )
    await BuySubscription.how_many.set()


@dp.message_handler(state=BuySubscription.how_many)
async def get_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer = message.text
    await state.update_data(how_many=answer)
    data = await state.get_data()
    worker_quantity = data.get('how_many')
    days = data.get('how_long')

    if not await payment_validator(worker_quantity, days):
        await state.finish()
        return await message.answer('Неправильные данные')

    await state.finish()
    amount = await calculate_price(worker_quantity, days)
    await form_bill(message, user_id, amount)


@dp.message_handler(commands=['delete'])
async def delete_worker(message: types.Message):
    """Start deleting a task"""
    await message.answer('Введи имя задачи')
    await DeleteWorker.delete_worker_name.set()


@dp.message_handler(state=DeleteWorker.delete_worker_name)
async def delete_name(message: types.Message, state: FSMContext) -> None:
    """Deleting a task"""
    answer = message.text
    await state.update_data(set_worker_name=answer)
    data = await state.get_data()
    worker_name = data.get('set_worker_name')

    db_resp = await delete_data(message.from_user.id, worker_name)
    await disable_track(message.from_user.id)
    await message.answer(db_resp)
    await state.finish()


@dp.message_handler(commands=['add'], state="*")
async def set_worker(message: types.Message) -> None:
    """Start adding a task"""
    await message.answer('Введи имя задачи')
    await SetWorker.set_worker_name.set()


@dp.message_handler(state=SetWorker.set_worker_name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    """Add task name"""
    answer = message.text
    await state.update_data(set_worker_name=answer)
    await message.answer('Отправьте URL')
    await SetWorker.set_worker_url.set()


@dp.message_handler(state=SetWorker.set_worker_url)
async def get_url(message: types.Message, state: FSMContext) -> types.Message:
    """Add task URL and finish"""
    answer = message.text
    await state.update_data(set_worker_url=answer)
    data = await state.get_data()
    name = data.get('set_worker_name')
    url = data.get('set_worker_url')

    if not await url_validator(url):
        await state.finish()
        return await message.answer('Неправильный URL')

    await message.answer(f'Добавляем {name} в нашу базу..')
    await insert_values(message.from_user.id, f"'{name}'", f"'{url}'")
    await message.answer('Отлично!\n'
                         'Введите /start_track, чтобы начать слежение\n '
                         '/add, чтобы добавить еще одно объявление')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
