from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTask(StatesGroup):
    name = State()
    url = State()


class DeleteTask(StatesGroup):
    name = State()


class BuySubscription(StatesGroup):
    system = State()
    days = State()
    advertisements = State()
    check = State()
    payment = State()
