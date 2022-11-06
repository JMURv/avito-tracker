from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_task = KeyboardButton('Добавить задачу')
stop_task = KeyboardButton('Остановить задачу')
info = KeyboardButton('Инфо')


keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.row(add_task, stop_task)
