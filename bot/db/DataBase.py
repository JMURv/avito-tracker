import os
from datetime import datetime
import asyncpg
from asyncpg import exceptions


DSN = os.getenv("DSN")


class DBConnect:
    def __init__(self):
        self.dsn = os.getenv("DSN")
        self.pool = None

    async def connect(self):
        # return await asyncpg.connect(self.dsn)
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=10,
                max_size=10,
            )


class DBTracking():
    async def enable_track(self, user_id: int) -> None:
        """Tracking. Enable it."""
        conn = await asyncpg.connect(DSN)
        update_query = f"""
            UPDATE users
            SET is_tracking = 1
            WHERE user_id = {user_id};
            """
        await conn.execute(update_query)
        await conn.close()

    async def disable_track(self, user_id: int) -> None:
        """Tracking. Disable it and remove results."""
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

    async def is_exist(self, user_id: int) -> bool:
        """Tracking. Read users result if it exists"""
        conn = await asyncpg.connect(DSN)
        query = f"""
        SELECT *
        FROM results
        WHERE user_id = {user_id}
        """
        data = await conn.fetch(query)
        await conn.close()
        return True if len(data) > 0 else False

    async def read_result(self, user_id: int, task_name: str) -> list:
        """Tracking. Check users last result"""
        conn = await asyncpg.connect(DSN)
        query = f"""
        SELECT first_name
        FROM results
        WHERE user_id = {user_id}
        AND task_name = '{task_name}'
        """
        data = await conn.fetch(query)
        ready_data = [task[0] for task in data]
        await conn.close()
        return ready_data

    async def register_first_result(
            self, user_id: int, task_name: str, first_result_name: str):
        """Tracking. Register a first result for user task"""
        conn = await asyncpg.connect(DSN)
        reg_query = f"""
        INSERT INTO results
        (USER_ID, TASK_NAME, FIRST_NAME)
        VALUES ({user_id}, '{task_name}', '{first_result_name}');
        """
        await conn.execute(reg_query)
        await conn.close()


class DBPayment(DBConnect):
    async def worker_quantity_check(self, user_id: int) -> int:
        """CRUD Payment. Read how many workers are allowed."""
        conn = await asyncpg.connect(DSN)
        now = str(datetime.now()).split(' ')[0]
        workers_query = f"""
                    SELECT workers_quantity
                    FROM subscribers
                    WHERE user_id = {user_id}
                    AND end_date > '{now}';"""
        data = await conn.fetchval(workers_query)
        await conn.close()
        return data

    async def is_subscriber(self, user_id: int) -> bool:
        """CRUD Payment. Read if user is subscriber or not."""
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

    async def create_new_subscriber(
            self, user_id: int, now, end, worker_quantity: dict) -> None:
        """CRUD Payment. Create a subscriber."""
        conn = await asyncpg.connect(DSN)
        reg_query = f"""
                INSERT INTO subscribers
                (user_id, purchase_date, end_date, workers_quantity)
                VALUES ({user_id}, '{now}', '{end}', {worker_quantity});
                """
        await conn.execute(reg_query)
        await conn.close()


class DBCommands(DBTracking, DBPayment):
    async def get_active_users(self) -> list:
        """CRUD operation. Read all active users"""
        conn = await asyncpg.connect(DSN)
        query = """
        SELECT user_id
        FROM users
        WHERE is_tracking = 1
        """
        data = await conn.fetch(query)
        ready_data = [user_id[0] for user_id in data]
        await conn.close()
        return ready_data

    async def is_alive(self, user_id: int):
        conn = await asyncpg.connect(DSN)
        query = f"""
        SELECT is_tracking
        FROM users
        WHERE user_id = {user_id}
        """
        await conn.close()
        return await conn.fetchval(query)

    async def create_user(self, user_id: int) -> bool:
        """CRUD operation. Create a user."""
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

    async def delete_task(self, user_id: int, task_name: str) -> str:
        """CRUD operation. Deleting a task"""
        conn = await asyncpg.connect(DSN)
        delete_query = f"""
        DELETE FROM workers
        WHERE USER_ID = {user_id}
        AND TASK_NAME = '{task_name}';"""
        delete_result_query = f"""
        DELETE FROM results
        WHERE USER_ID = {user_id}
        AND TASK_NAME = '{task_name}';"""
        resp = await conn.execute(delete_query)
        await conn.execute(delete_result_query)
        await conn.close()
        if resp[-1] == '0':
            return f'Неправильное имя задачи {task_name}'
        else:
            return f'Успешное удаление {task_name}'

    async def create_task(self, user_id: int, name: str, url: str) -> None:
        """CRUD operation. Creating a task"""
        conn = await asyncpg.connect(DSN)
        insert_query = f"""
        INSERT INTO workers
        (USER_ID, TASK_NAME, TASK_URL)
        VALUES ({user_id}, {name}, {url});
        """
        await conn.execute(insert_query)
        await conn.close()

    async def read_tasks(self, user_id: int) -> dict:
        """CRUD operation. Reading a users tasks"""
        conn = await asyncpg.connect(DSN)
        read_query = f"""
        SELECT TASK_NAME, TASK_URL
        FROM workers
        WHERE USER_ID = {user_id}"""
        data = await conn.fetch(read_query)
        result = {row[0]: row[1] for row in data}
        await conn.close()
        return result

    async def read_user_task_names(self, user_id: int) -> list:
        conn = await asyncpg.connect(DSN)
        query = f"""
        SELECT TASK_NAME
        FROM workers
        WHERE USER_ID = {user_id}"""
        await conn.close()
        return [name[0] for name in await conn.fetch(query)]

    async def read_user_task(self, user_id: int) -> str:
        """CRUD operation. Reading a users tasks names"""
        conn = await asyncpg.connect(DSN)
        check_query = f"""
        SELECT TASK_NAME, TASK_URL
        FROM workers
        WHERE USER_ID = {user_id}"""
        data = await conn.fetch(check_query)
        result = [
            f"{name[0]} || {name[1]}"
            for name in data
        ]
        await conn.close()
        return ', \n'.join(result)
