from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('Добавить задачу')
b2 = KeyboardButton('Удалить задачу')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.row(b1, b2)
