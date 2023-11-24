from db import DBCommands


DB = DBCommands()
TRIES = 7


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
    return one_day_price * days
