from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTask(StatesGroup):
    name = State()
    url = State()


class DeleteTask(StatesGroup):
    name = State()


class BuySubscription(StatesGroup):
    how_long = State()
    how_many = State()
