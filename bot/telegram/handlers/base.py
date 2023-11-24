from loguru import logger
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from telegram.initializer import dp, bot
from telegram.keyboards import (
    main_markup,
    cancel,
    my_tasks,
)
from db import DBCommands


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
    # TODO: Логирование
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
        return


async def bot_start():
    await dp.start_polling(bot)
