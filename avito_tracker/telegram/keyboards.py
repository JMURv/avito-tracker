from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def inline_kb(url: str, text='Ссылка') -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=text, url=url)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    return keyboard


add_task = KeyboardButton("✅ Добавить задачу")
delete_task = KeyboardButton("❌ Удалить задачу")
check_tasks = KeyboardButton("📋 Мои задачи")
stop_all_tasks = KeyboardButton("⚠ Остановить слежение")
start_all_tasks = KeyboardButton("📡 Запустить слежение")
buy_subscription = KeyboardButton("⭐ Купить подписку")

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(add_task, delete_task, check_tasks)\
    .row(start_all_tasks, buy_subscription)
short_kb = ReplyKeyboardMarkup(resize_keyboard=True)
short_kb.row(stop_all_tasks)

five_workers = KeyboardButton("5")
ten_workers = KeyboardButton("10")
fifthteen_workers = KeyboardButton("15")

keyboard_workers = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_workers.row(five_workers, ten_workers, fifthteen_workers)
