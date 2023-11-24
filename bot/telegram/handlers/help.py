from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from telegram.initializer import dp
from telegram.keyboards import support, main_markup


@dp.callback_query_handler(lambda query: query.data == support)
async def cmd_sos(query: CallbackQuery):
    try:
        await query.message.edit_caption(
            caption='Служба поддержки отвечает ежедневно с 10:00 до 19:00 по Москве: @JMURv',
            reply_markup=await main_markup()
        )
    except MessageNotModified:
        return
