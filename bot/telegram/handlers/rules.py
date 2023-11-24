from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from telegram.initializer import dp
from telegram.keyboards import rules, main_markup


@dp.callback_query_handler(lambda query: query.data == rules)
async def rules_handler(query: CallbackQuery):
    rules_text = """
        ✅ | ПОКУПАЯ ТОВАР, ВЫ АВТОМАТИЧЕСКИ СОГЛАШАЕТЕСЬ СО ВСЕМИ ПРАВИЛАМИ!\n
        ═══════════════════════════════════════════
        🥸 | Гарантируем сохранность ваших персональных данных. Храним только ваш ID.
        🦆 |Гарантируем обратную связь и полную поддержку в непредвиденных случаях.
        🎥 | Всегда имейте запись (видеодоказательство), чтобы мы могли обработать вашу заявку.
        💸 | Баланс с бота не возвращаем!
        """
    try:
        await query.message.edit_caption(
            caption=rules_text,
            reply_markup=await main_markup()
        )
    except MessageNotModified:
        return
