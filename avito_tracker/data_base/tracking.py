from avito_tracker.data_base.config import DSN
from asyncpg import exceptions
import asyncpg


async def register_user(user_id):
    conn = await asyncpg.connect(DSN)
    is_registered = False
    try:
        reg_query = f"""
            INSERT INTO users
            (user_id, is_tracking)
            VALUES ({user_id}, {0});
            """
        await conn.execute(reg_query)
    except exceptions.UniqueViolationError:
        is_registered = True
    finally:
        await conn.close()
        return is_registered


async def is_tracking_now(user_id):
    conn = await asyncpg.connect(DSN)
    query = f"""
    SELECT is_tracking
    FROM users
    WHERE user_id = {user_id};"""
    data = await conn.fetchval(query)
    await conn.close()
    return data


async def enable_track(user_id):
    conn = await asyncpg.connect(DSN)
    update_query = f"""
        UPDATE users
        SET is_tracking = 1
        WHERE user_id = {user_id};
        """
    await conn.execute(update_query)
    await conn.close()


async def disable_track(user_id):
    conn = await asyncpg.connect(DSN)
    insert_query = f"""
    UPDATE users
    SET is_tracking = 0
    WHERE user_id = {user_id};
    """
    await conn.execute(insert_query)
    await conn.close()
