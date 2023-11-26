from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from telegram.initializer import dp
from telegram.keyboards import faq, main_markup


FAQ_TEXT = """
1. Сколько я могу завести объявлений?
Ответ: Не более 1 объявления для бесплатного аккаунта.

2. Какая ссылка требуется для трекинга?
Ответ: Ссылка из поиска авито, но есть несколько тонкостей:
    2.1 Выбирайте отображение списком (выбрано по усолчанию)
    2.2 Требуется установить сортировку по дате

3. Что я могу настроить?
Ответ: Можно настраивать всё, что предлагает сервис: цену, доставку и тд.
"""


@dp.callback_query_handler(lambda query: query.data == faq)
async def faq_handler(query: CallbackQuery):
    try:
        await query.message.edit_caption(
            caption=FAQ_TEXT,
            reply_markup=await main_markup()
        )
    except MessageNotModified:
        return
