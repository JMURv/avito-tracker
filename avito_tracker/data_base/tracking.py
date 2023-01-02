from avito_tracker.data_base.config import DSN
from asyncpg import exceptions
import asyncpg


async def register_first_result(
        user_id: int, task_name: str, fres_name: str) -> None:
    conn = await asyncpg.connect(DSN)
    reg_query = f"""
    INSERT INTO results
    (USER_ID, TASK_NAME, FIRST_NAME)
    VALUES ({user_id}, '{task_name}', '{fres_name}');
    """
    await conn.execute(reg_query)
    await conn.close()


async def check_first_result(user_id: int, task_name: str) -> None:
    conn = await asyncpg.connect(DSN)
    query = f"""
    SELECT first_name
    FROM results
    WHERE user_id = {user_id}
    AND task_name = '{task_name}'
    """
    data = await conn.fetchval(query)
    await conn.close()
    return data


async def update_result(user_id: int, task_name: str, new_name: str) -> None:
    conn = await asyncpg.connect(DSN)
    update_query = f"""
    UPDATE results
    SET first_name = '{new_name}'
    WHERE user_id = {user_id}
    AND task_name = '{task_name}'
    """
    await conn.execute(update_query)
    await conn.close()


async def check_if_exists(user_id: int) -> bool:
    """Проверить наличие уже просчитаных результатов"""
    conn = await asyncpg.connect(DSN)
    query = f"""
    SELECT *
    FROM results
    WHERE user_id = {user_id}
    """
    data = await conn.fetch(query)
    await conn.close()
    return True if len(data) > 0 else False


async def register_user(user_id: int) -> bool:
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


async def is_tracking_now(user_id: int):
    conn = await asyncpg.connect(DSN)
    query = f"""
    SELECT is_tracking
    FROM users
    WHERE user_id = {user_id};"""
    data = await conn.fetchval(query)
    await conn.close()
    return data


async def enable_track(user_id: int) -> None:
    conn = await asyncpg.connect(DSN)
    update_query = f"""
        UPDATE users
        SET is_tracking = 1
        WHERE user_id = {user_id};
        """
    await conn.execute(update_query)
    await conn.close()


async def disable_track(user_id: int) -> None:
    conn = await asyncpg.connect(DSN)
    insert_query = f"""
    UPDATE users
    SET is_tracking = 0
    WHERE user_id = {user_id};
    """
    delete_query = f"""
    DELETE FROM results
    WHERE USER_ID = {user_id};"""
    await conn.execute(insert_query)
    await conn.execute(delete_query)
    await conn.close()


def get_ready_id(data):
    return data[0]


async def get_active_users() -> list:
    conn = await asyncpg.connect(DSN)
    query = """
    SELECT user_id
    FROM users
    WHERE is_tracking = 1
    """
    data = await conn.fetch(query)
    ready_data = list(map(get_ready_id, data))
    await conn.close()
    return ready_data
