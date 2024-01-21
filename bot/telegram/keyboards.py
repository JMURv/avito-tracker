from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.callbacks import task_cb


main_menu = "◀️ Главное меню"
add_task = "✅ Добавить объявление"
delete_task = "❌ Удалить объявление"
my_tasks = "📋 Мои задачи"
stop_all_tasks = "⚠ Остановить слежение"
start_all_tasks = "📡 Запустить слежение"
buy_subscription = "⭐ Купить подписку"
support = "🆘 Помощь"
rules = "📜 Правила"
faq = "❓ FAQ"

cancel = "❌"
back = "◀️"

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


async def all_user_tasks_markup(tasks_names):
    markup = InlineKeyboardMarkup(selective=True)
    for task_name in tasks_names:
        markup.add(
            InlineKeyboardButton(
                task_name,
                callback_data=task_cb.new(
                    name=task_name,
                    action='remove'
                )
            )
        )
    markup.row(
        InlineKeyboardButton(text=back, callback_data=back),
        InlineKeyboardButton(text=add_task, callback_data=add_task),
    )
    return markup


async def accept_or_back_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.row(
        InlineKeyboardButton(text=back, callback_data=back),
        InlineKeyboardButton(text=accept, callback_data=accept),
    )
    return markup


async def main_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=my_tasks, callback_data=my_tasks),
        InlineKeyboardButton(text=buy_subscription, callback_data=buy_subscription)
    )
    markup.add(
        InlineKeyboardButton(text=start_all_tasks, callback_data=start_all_tasks),
        InlineKeyboardButton(text=stop_all_tasks, callback_data=stop_all_tasks)
    )
    markup.add(
        InlineKeyboardButton(text=faq, callback_data=faq),
        InlineKeyboardButton(text=rules, callback_data=rules),
        InlineKeyboardButton(text=support, callback_data=support),
    )
    return markup


async def active_tracking_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.add(
        InlineKeyboardButton(text=my_tasks, callback_data=my_tasks),
        InlineKeyboardButton(text=buy_subscription, callback_data=buy_subscription)
    )
    markup.add(
        InlineKeyboardButton(text=stop_all_tasks, callback_data=stop_all_tasks)
    )
    markup.add(
        InlineKeyboardButton(text=faq, callback_data=faq),
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
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def payment_days_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.row(
        InlineKeyboardButton(text=available_days[0], callback_data=available_days[0]),
        InlineKeyboardButton(text=available_days[1], callback_data=available_days[1]),
    )
    markup.row(
        InlineKeyboardButton(text=available_days[2], callback_data=available_days[2]),
        InlineKeyboardButton(text=available_days[3], callback_data=available_days[3]),
    )
    markup.add(
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def payment_tasks_markup():
    markup = InlineKeyboardMarkup(selective=True)
    markup.row(
        InlineKeyboardButton(text=available_tasks[0], callback_data=available_tasks[0]),
        InlineKeyboardButton(text=available_tasks[1], callback_data=available_tasks[1]),
        InlineKeyboardButton(text=available_tasks[2], callback_data=available_tasks[2]),
    )
    markup.add(
        InlineKeyboardButton(text=back, callback_data=back)
    )
    return markup


async def item_inline_kb(url: str, text='Ссылка') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(selective=True, row_width=1)
    keyboard.add(
        InlineKeyboardButton(text=main_menu, callback_data=main_menu),
        InlineKeyboardButton(text=text, url=url)
    )
    return keyboard
