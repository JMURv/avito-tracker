from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteTask(StatesGroup):
    confirm = State()


class AddTask(StatesGroup):
    name = State()
    url = State()
    confirm = State()


class BuySubscription(StatesGroup):
    system = State()
    days = State()
    advertisements = State()
    check = State()
    payment = State()
