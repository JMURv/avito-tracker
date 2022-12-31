import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import types

from avito_tracker.data_base.payment import register_new_subscriber
from avito_tracker.telegram.keyboards import inline_kb
from telegram.initializer import dp
from yoomoney import Client, Quickpay

TRIES = 4

load_dotenv(find_dotenv())
token = getenv('yoomoney_token')
client = Client(token)


async def calculate_price(worker_quantity: str, days: str) -> int:
    worker_quantity, days = int(worker_quantity), int(days)
    if worker_quantity == 5:
        one_day_price = 15
        if days >= 15:
            one_day_price = 10

    if worker_quantity == 10:
        one_day_price = 20
        if days >= 15:
            one_day_price = 15

    if worker_quantity == 15:
        one_day_price = 30
        if days >= 15:
            one_day_price = 25
    # noinspection PyUnboundLocalVariable
    return one_day_price*days


async def form_bill(message: types.Message, user_id: int, subscription_data: dict):
    amount = subscription_data.get('amount')

    now = str(datetime.now()).split(' ')[0]  # 2022-12-30
    end_date = str(datetime.now() + timedelta(days=subscription_data.get('days'))).split(' ')[0]

    label = f"{user_id}.{now}"
    quickpay = Quickpay(
                receiver="4100115677330952",
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=amount,
                label=label
                )
    payment_url = quickpay.redirected_url
    inline = await inline_kb(payment_url, 'Купить подписку')
    await dp.bot.send_message(
        chat_id=user_id,
        text=f"Дней подписки: {subscription_data.get('days')}\n"
             f"Количество активных объявлений: {subscription_data.get('worker_quantity')}\n"
             f"Итоговая цена: {amount}",
        reply_markup=inline
    )
    await sleep(40)
    for check in range(TRIES):
        history = client.operation_history(label=label)
        try:
            status = history.operations[0].status
        except IndexError:
            status = 'unsuccess'
        if status == 'success':
            await register_new_subscriber(user_id, now, end_date, subscription_data)
            return await message.answer("Успех!")
        else:
            await sleep(20)
    return await message.answer("Неудача!")


# async def test(label: str):
#     for check in range(TRIES):
#         history = client.operation_history(label=label)
#         try:
#             status = history.operations[0].status
#         except IndexError:
#             print('Waiting')
#             status = 'unsuccess'
#         if status == 'success':
#             return '+'
#         else:
#             await sleep(10)
#     return '-'

print(str(datetime.now()).split(' ')[0])
print( str(datetime.now() + timedelta(days=10)).split(' ')[0] )