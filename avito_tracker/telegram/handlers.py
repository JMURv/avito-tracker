
from aiogram import types
from aiogram.dispatcher import FSMContext

from avito_tracker.telegram import States
from avito_tracker.telegram.initializer import dp
from avito_tracker.telegram.keyboards import main_kb, keyboard_workers

from avito_tracker.telegram.payment import form_bill, calculate_price
from avito_tracker.validators import url_validator, payment_validator
from avito_tracker.parsing.tracking import worker_checker

from avito_tracker.data_base.DataBase import DBCommands
DB = DBCommands()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    is_registered = await DB.create_user(message.from_user.id)
    if not is_registered:
        await message.answer(
            "Привет 👋\n"
            "Я бот, который следит за объявлениями за тебя!\n"
            "Прочитай правила и FAQ перед использованием:"
            " /help",
            reply_markup=main_kb)
    else:
        name = message.from_user.username
        await message.answer(
            f"С возвращением, {name} 👋\n"
            "Я тебя помню! Как дела?",
            reply_markup=main_kb)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message) -> None:
    await message.answer(
        "FAQ:\n"
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
        reply_markup=main_kb)


@dp.message_handler()
async def reply_text(message: types.Message) -> None:
    if message.text in ('✅ Добавить задачу', '/add'):
        await set_worker(message)
    if message.text in ('❌ Удалить задачу', '/delete'):
        await delete_worker(message)
    if message.text == '📋 Мои задачи':
        tasks = await DB.read_user_task(message.from_user.id)
        await message.answer(
            f"Ваши задачи: {tasks}",
            reply_markup=main_kb)
    if message.text in ('📡 Запустить слежение', '/start_track'):
        await worker_checker(message)
    if message.text == '⚠ Остановить слежение':
        await message.answer('Это может занять какое-то время..')
        await DB.disable_track(message.from_user.id)
        await message.answer(
            'Готово!',
            reply_markup=main_kb)
    if message.text == '⭐ Купить подписку':
        await buy_subscription(message)


@dp.message_handler(commands=['buy'])
async def buy_subscription(message: types.Message):

    if await DB.is_subscriber(message.from_user.id):
        return await message.answer(
            'У вас уже есть подписка!',
            reply_markup=main_kb
        )

    await message.answer(
        'Сколько дней подписки хотите?\n'
        'Напишите количество.'
    )
    await States.BuySubscription.how_long.set()


@dp.message_handler(state=States.BuySubscription.how_long)
async def get_time(message: types.Message, state: FSMContext) -> None:
    answer = message.text
    await state.update_data(how_long=answer)
    await message.answer(
        'Как много объявлений хотите отслежвать?',
        reply_markup=keyboard_workers
    )
    await States.BuySubscription.how_many.set()


@dp.message_handler(state=States.BuySubscription.how_many)
async def get_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer = message.text
    await state.update_data(how_many=answer)
    data = await state.get_data()

    worker_quantity, days = data.get('how_many'), data.get('how_long')
    if not await payment_validator(worker_quantity, days):
        await state.finish()
        return await message.answer(
            'Неправильные данные',
            reply_markup=main_kb
        )

    await state.finish()
    subscription_data = {
        'worker_quantity': worker_quantity,
        'days': days,
        'amount': await calculate_price(worker_quantity, days)
    }
    await form_bill(message, user_id, subscription_data)


@dp.message_handler(commands=['delete'])
async def delete_worker(message: types.Message):
    """Start deleting a task"""
    await message.answer('Введи имя задачи')
    await States.DeleteWorker.delete_worker_name.set()


@dp.message_handler(state=States.DeleteWorker.delete_worker_name)
async def delete_name(message: types.Message, state: FSMContext) -> None:
    """Deleting a task"""
    answer = message.text
    await state.update_data(set_worker_name=answer)
    data = await state.get_data()
    worker_name = data.get('set_worker_name')

    db_resp = await DB.delete_task(message.from_user.id, worker_name)
    await message.answer(db_resp)
    await state.finish()


@dp.message_handler(commands=['add'], state="*")
async def set_worker(message: types.Message) -> None:
    """Start adding a task"""
    await message.answer('Введи имя задачи')
    await States.SetWorker.set_worker_name.set()


@dp.message_handler(state=States.SetWorker.set_worker_name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    """Add task name"""
    answer = message.text
    await state.update_data(set_worker_name=answer)
    await message.answer('Отправьте URL')
    await States.SetWorker.set_worker_url.set()


@dp.message_handler(state=States.SetWorker.set_worker_url)
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
    await DB.create_task(message.from_user.id, f"'{name}'", f"'{url}'")
    await message.answer(
        'Отлично!\n'
        'Введите /start_track, чтобы начать слежение\n '
        '/add, чтобы добавить еще одно объявление')
    await state.finish()
