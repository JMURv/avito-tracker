from aiogram.dispatcher.filters.state import StatesGroup, State


class SetWorker(StatesGroup):
    set_worker_name = State()
    set_worker_url = State()


class DeleteWorker(StatesGroup):
    set_worker_name = State()
