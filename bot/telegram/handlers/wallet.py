import os
import datetime

from data.crystalpay_sdk import CrystalPAY, InvoiceType
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from telegram.handlers.base import send_image
from telegram.states import BuySubscription
from telegram.initializer import dp
from telegram.keyboards import (
    main_markup,
    back_markup,
    buy_subscription,
    payment_systems_markup,
    crystal_pay,
    accept_or_back_markup,
    accept,
    back,
    cancel,
)
from telegram.payment import calculate_price
from addons.validators import payment_validator
from db import DBCommands


@dp.callback_query_handler(lambda query: query.data == buy_subscription)
async def buy_subscription_handler(query: CallbackQuery) -> Message:
    db = DBCommands()
    if await db.is_subscriber(query.from_user.id):
        return await query.message.edit_caption(
            caption='У вас уже есть подписка!',
            reply_markup=await main_markup()
        )
    await BuySubscription.system.set()
    return await query.message.answer(
        text='Выберите платёжную систему',
        reply_markup=await payment_systems_markup()
    )


@dp.callback_query_handler(lambda query: query.data in (crystal_pay, cancel), state=BuySubscription.system)
async def process_payment_system(query: CallbackQuery, state: FSMContext) -> Message:
    if query.data == cancel:
        await state.finish()
        return await send_image(
            cid=query.from_user.id,
            caption="",
            markup=await main_markup()
        )
    async with state.proxy() as data:
        data["payment_system"] = query.data
    await BuySubscription.days.set()
    return await query.message.answer(
        text='Сколько дней подписки хотите?\n'
        'Напишите количество.',
        reply_markup=await back_markup()
    )


@dp.message_handler(state=BuySubscription.days)
async def get_time(message: Message, state: FSMContext) -> Message:
    if message.text == back:
        await BuySubscription.system.set()
        return await message.answer(
            text='Выберите платёжную систему',
            reply_markup=await payment_systems_markup()
        )
    async with state.proxy() as data:
        data['how_long'] = message.text
    await BuySubscription.advertisements.set()
    return await message.answer(
        text='Как много объявлений хотите отслежвать?',
        reply_markup=await back_markup()
    )


@dp.message_handler(state=BuySubscription.advertisements)
async def get_tasks_quantity(message: Message, state: FSMContext) -> Message:
    if message.text == back:
        await BuySubscription.days.set()
        return await message.answer(
            text='Сколько дней подписки хотите?\n',
            reply_markup=await back_markup()
        )
    async with state.proxy() as data:
        data['tasks_quantity'] = message.text
        tasks_quantity, days = data.get('tasks_quantity'), data.get('how_long')
        price = await calculate_price(tasks_quantity, days)
        data['price'] = price

    if not await payment_validator(tasks_quantity, days):
        await state.finish()
        return await message.answer(
            text='Неправильные данные',
            reply_markup=await main_markup()
        )
    await BuySubscription.check.set()
    return await message.answer(
        text=f"Подтвердите данные: \n"
             f"Кол-во дней: {days}\n"
             f"Кол-во объявлений: {tasks_quantity}\n\n"
             f"Итоговая стоимость: {price}р",
        reply_markup=await accept_or_back_markup()
    )


@dp.callback_query_handler(lambda query: query.data in (accept, back), state=BuySubscription.check)
async def check_payment_info(query: CallbackQuery, state: FSMContext):
    if query.data == back:
        await BuySubscription.advertisements.set()
        return await query.message.answer(
            text='Как много объявлений хотите отслежвать?',
            reply_markup=await back_markup()
        )
    if query.data == accept:
        async with state.proxy() as data:
            crystalpay = CrystalPAY(
                auth_login=os.getenv("CRYSTALPAY_LOGIN"),
                auth_secret=os.getenv("CRYSTALPAY_SECRET_KEY"),
                salt=os.getenv("CRYSTALPAY_SALT_KEY"),
            )
            response = crystalpay.Invoice.create(
                amount=data.get("price"),
                type_=InvoiceType.purchase,
                lifetime=15
            )
            data["pay_id"] = response.get("id")
            payment_url = response.get("url")
        await BuySubscription.payment.set()
        await query.message.answer(
            text=f"Ссылка для оплаты: {payment_url}",
        )
        return await query.message.answer(
            text=f"Подтвердите оплату по ссылке?",
            reply_markup=await accept_or_back_markup()
        )


@dp.callback_query_handler(lambda query: query.data in (accept, back), state=BuySubscription.payment)
async def process_payment(query: CallbackQuery, state: FSMContext):
    if query.data == back:
        await state.finish()
        await query.answer(text='Отмена оплаты')
        return await send_image(
            cid=query.from_user.id,
            caption="",
            markup=await main_markup()
        )
    if query.data == accept:
        async with state.proxy() as data:
            payment_system = data.get('payment_system')
            pay_id = data.get('pay_id')
        if payment_system == crystal_pay:
            client = CrystalPAY(
                auth_login=os.getenv("CRYSTALPAY_LOGIN"),
                auth_secret=os.getenv("CRYSTALPAY_SECRET_KEY"),
                salt=os.getenv("CRYSTALPAY_SALT_KEY")
            )
            status = client.Invoice.getinfo(id=pay_id).get("state")
            if status == "notpayed" or status == "processing":
                await waiting_for_a_payment(query)
            elif status == "payed":
                await success_payment(query, state)
            elif status in ("wrongamount", "failed"):
                await error_payment(query, state)


async def error_payment(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await send_image(
        cid=query.from_user.id,
        caption=f'Ссылка истекла или произошла ошибка, попробуйте повторить процесс пополнения кошелька.',
        markup=await main_markup()
    )


async def success_payment(query: CallbackQuery, state: FSMContext):
    db = DBCommands()
    async with state.proxy() as data:
        now = datetime.datetime.now()
        end_date = now + datetime.timedelta(
            days=int(data.get("how_long"))
        )
        await db.create_new_subscriber(
            user_id=query.from_user.id,
            now=now,
            end=end_date,
            worker_quantity=data.get("tasks_quantity")
        )
    await state.finish()
    await send_image(
        cid=query.from_user.id,
        caption=f'Оплата прошла успешно!',
        markup=await main_markup()
    )


async def waiting_for_a_payment(query: CallbackQuery):
    return await query.answer(
        text=f'Счёт ожидает оплаты',
    )
