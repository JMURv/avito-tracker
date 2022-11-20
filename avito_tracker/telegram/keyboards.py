from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def inline_kb(url):
    button = InlineKeyboardButton(text="Ссылка", url=url)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    return keyboard


add_task = KeyboardButton("✅ Добавить задачу")
delete_task = KeyboardButton("❌ Удалить задачу")
check_tasks = KeyboardButton("📋 Мои задачи")
stop_all_tasks = KeyboardButton("⚠ Остановить слежение")
start_all_tasks = KeyboardButton("📡 Запустить слежение")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.row(add_task, delete_task, check_tasks)\
    .row(start_all_tasks)

keyboard_short = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_short.row(stop_all_tasks)
