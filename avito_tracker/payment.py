from asyncio import sleep
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import types

from avito_tracker.data_base.DataBase import DBCommands
from avito_tracker.telegram.keyboards import inline_kb, keyboard_client
from telegram.initializer import dp
from yoomoney import Client, Quickpay

DB = DBCommands()
TRIES = 7

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


async def form_bill(
        message: types.Message, user_id: int, data: dict) -> types.Message:
    amount = data.get('amount')
    days = data.get('days')

    now = str(datetime.now()).split(' ')[0]  # 2022-12-31
    end_date = str(datetime.now() + timedelta(days=int(days))).split(' ')[0]

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
        text=f"Дней подписки: {data.get('days')}\n"
             f"Количество активных объявлений: {data.get('worker_quantity')}\n"
             f"Итоговая цена: {amount}р\n\n"
             f"Ссылка действительна 3 минуты с момента отправки",
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
            await DB.create_new_subscriber(user_id, now, end_date, data)
            return await message.answer(
                "Успешная оплата!\n"
                "Наслаждайтесь подпиской 💕",
                reply_markup=keyboard_client
            )
        else:
            await sleep(20)
    return await message.answer(
        "Не дождался оплаты :(\n"
        "Попробуйте еще раз",
        reply_markup=keyboard_client
    )
