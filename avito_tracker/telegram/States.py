from aiogram.dispatcher.filters.state import StatesGroup, State


class SetWorker(StatesGroup):
    set_worker_name = State()
    set_worker_url = State()


class DeleteWorker(StatesGroup):
    delete_worker_name = State()


class BuySubscription(StatesGroup):
    how_long = State()
    how_many = State()
