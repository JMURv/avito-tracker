from avito_tracker.data_base.config import DSN
import asyncpg


async def register_new_subscriber(user_id, now, end, subscription_data):
    conn = await asyncpg.connect(DSN)
    workers_quantity = subscription_data.get('workers_quantity')
    reg_query = f"""
    INSERT INTO subscribers
    (user_id, purchase_date, end_date, workers_quantity)
    VALUES ({user_id}, '{now}', '{end}', {workers_quantity});
    """
    await conn.execute(reg_query)
    await conn.close()


async def check_for_subscription(user_id):
    pass

