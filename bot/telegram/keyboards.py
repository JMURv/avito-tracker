from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


add_task = "✅ Добавить объявление"
delete_task = "❌ Удалить объявление"
my_tasks = "📋 Мои задачи"
stop_all_tasks = "⚠ Остановить слежение"
start_all_tasks = "📡 Запустить слежение"
buy_subscription = "⭐ Купить подписку"
support = "Помощь"
rules = "Правила"

cancel = "Отмена"
back = "Назад"

accept = "✅"
crystal_pay = "💎 Crystal Pay"

available_days = [
    "5",
    "10",
    "20",
    "30"
]

available_tasks = [
    "5",
    "10",
    "15"
]


async def accept_or_back_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.row(
        InlineKeyboardButton(text=accept, callback_data=accept),
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def main_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=add_task, callback_data=add_task),
        InlineKeyboardButton(text=delete_task, callback_data=delete_task)
    )
    markup.add(
        InlineKeyboardButton(text=my_tasks, callback_data=my_tasks),
        InlineKeyboardButton(text=buy_subscription, callback_data=buy_subscription)
    )
    markup.add(
        InlineKeyboardButton(text=start_all_tasks, callback_data=start_all_tasks),
        InlineKeyboardButton(text=stop_all_tasks, callback_data=stop_all_tasks)
    )
    markup.add(
        InlineKeyboardButton(text=rules, callback_data=rules),
        InlineKeyboardButton(text=support, callback_data=support)
    )
    return markup


async def active_tracking_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=add_task, callback_data=add_task),
        InlineKeyboardButton(text=delete_task, callback_data=delete_task)
    )
    markup.add(
        InlineKeyboardButton(text=my_tasks, callback_data=my_tasks),
        InlineKeyboardButton(text=buy_subscription, callback_data=buy_subscription)
    )
    markup.add(
        InlineKeyboardButton(text=stop_all_tasks, callback_data=stop_all_tasks)
    )
    markup.add(
        InlineKeyboardButton(text=rules, callback_data=rules),
        InlineKeyboardButton(text=support, callback_data=support)
    )
    return markup


async def back_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def cancel_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=cancel, callback_data=cancel)
    )
    return markup


async def payment_systems_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=crystal_pay, callback_data=crystal_pay)
    )
    markup.add(
        InlineKeyboardButton(text=cancel, callback_data=cancel)
    )
    return markup


async def payment_days_markup():
    markup = InlineKeyboardMarkup(selective=True)
    for day in available_days:
        markup.add(
            InlineKeyboardButton(text=day, callback_data=day)
        )
    markup.add(
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def payment_tasks_markup():
    markup = InlineKeyboardMarkup(selective=True)
    for day in available_tasks:
        markup.add(
            InlineKeyboardButton(text=day, callback_data=day)
        )
    markup.add(
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def item_inline_kb(url: str, text='Ссылка') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(selective=True, row_width=1)
    keyboard.add(
        InlineKeyboardButton(text=stop_all_tasks, callback_data=stop_all_tasks),
        InlineKeyboardButton(text=text, url=url)
    )
    return keyboard