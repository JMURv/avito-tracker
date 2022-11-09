from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_task = KeyboardButton("✅ Добавить задачу")
delete_task = KeyboardButton("❌ Удалить задачу")
stop_all_tasks = KeyboardButton("⚠ Остановить слежение")
start_all_tasks = KeyboardButton("📡 Запустить слежение")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.row(add_task, delete_task)\
    .row(start_all_tasks)

keyboard_short = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_short.row(stop_all_tasks)
