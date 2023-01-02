from datetime import datetime
from avito_tracker.data_base.config import DSN
import asyncpg


async def register_new_subscriber(
        user_id: int, now: str, end: str, data: dict) -> None:
    conn = await asyncpg.connect(DSN)
    worker_quantity = data.get('worker_quantity')
    reg_query = f"""
    INSERT INTO subscribers
    (user_id, purchase_date, end_date, workers_quantity)
    VALUES ({user_id}, '{now}', '{end}', {worker_quantity});
    """
    await conn.execute(reg_query)
    await conn.close()


async def check_for_subscription(user_id: int) -> bool:
    conn = await asyncpg.connect(DSN)
    now = str(datetime.now()).split(' ')[0]
    check_query = f"""
    SELECT COUNT(*)
    FROM subscribers
    WHERE user_id = {user_id}
    AND end_date > '{now}';"""
    data = await conn.fetchval(check_query)
    await conn.close()
    return False if data == 0 else True


async def worker_quantity_check(user_id: int) -> int:
    conn = await asyncpg.connect(DSN)
    workers_query = f"""
        SELECT workers_quantity
        FROM subscribers
        WHERE user_id = {user_id};"""
    data = await conn.fetchval(workers_query)
    await conn.close()
    return data
