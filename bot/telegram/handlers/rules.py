from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from telegram.initializer import dp
from telegram.keyboards import rules, main_markup


RULES_TEXT = """
✅ | ПОКУПАЯ ТОВАР, ВЫ АВТОМАТИЧЕСКИ СОГЛАШАЕТЕСЬ СО ВСЕМИ ПРАВИЛАМИ!
═══════════════════════════════════════════
🥸 | Гарантируем сохранность ваших персональных данных. Храним только ваш ID.
🦆 |Гарантируем обратную связь и полную поддержку в непредвиденных случаях.
🎥 | Всегда имейте запись (видеодоказательство), чтобы мы могли обработать вашу заявку.
💸 | В случае отправки по неверным реквизитам или недостаточной суммы деньги не возвращаем!
"""


@dp.callback_query_handler(lambda query: query.data == rules)
async def rules_handler(query: CallbackQuery):
    try:
        await query.message.edit_caption(
            caption=RULES_TEXT,
            reply_markup=await main_markup()
        )
    except MessageNotModified:
        return
