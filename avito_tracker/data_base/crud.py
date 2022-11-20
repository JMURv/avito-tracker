from avito_tracker.data_base.config import DSN
import asyncpg


async def check_workers(user_id):
    conn = await asyncpg.connect(DSN)
    check_query = f"""
    SELECT TASK_NAME
    FROM workers
    WHERE USER_ID = {user_id}"""
    data = await conn.fetch(check_query)
    result = [name[0] for name in data]
    await conn.close()
    return ', '.join(result)


async def insert_values(user_id, name, url):
    conn = await asyncpg.connect(DSN)
    insert_query = f"""
    INSERT INTO workers
    (USER_ID, TASK_NAME, TASK_URL)
    VALUES ({user_id}, {name}, {url});
    """
    await conn.execute(insert_query)
    await conn.close()


async def read_data(user_id):
    conn = await asyncpg.connect(DSN)
    read_query = f"""
    SELECT TASK_NAME, TASK_URL
    FROM workers
    WHERE USER_ID = {user_id}"""
    data = await conn.fetch(read_query)
    result = {row[0]: row[1] for row in data}
    await conn.close()
    return result


async def delete_data(user_id, worker_name):
    conn = await asyncpg.connect(DSN)
    delete_query = f"""
    DELETE FROM workers
    WHERE USER_ID = {user_id}
    AND TASK_NAME = '{worker_name}';"""
    resp = await conn.execute(delete_query)
    await conn.close()
    if resp[-1] == '0':
        return f'Неправильное имя задачи {worker_name}'
    else:
        return f'Успешное удаление {worker_name}'
