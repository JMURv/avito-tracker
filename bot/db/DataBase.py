import os
from datetime import datetime
import asyncpg
from asyncpg import exceptions


class DBConnect:
    def __init__(self):
        self.dsn = os.getenv("DSN")
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=2,
                max_size=4
            )


class DBTracking(DBConnect):
    async def enable_track(self, user_id: int) -> None:
        """Tracking. Enable it."""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            update_query = f"""
                UPDATE users
                SET is_tracking = 1
                WHERE user_id = {user_id};
                """
            await conn.execute(update_query)

    async def disable_track(self, user_id: int) -> None:
        """Tracking. Disable it and remove results."""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
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

    async def is_exist(self, user_id: int) -> bool:
        """Tracking. Read users result if it exists"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT *
            FROM results
            WHERE user_id = {user_id}
            """
            data = await conn.fetch(query)
            return True if len(data) > 0 else False

    async def read_result(self, user_id: int, task_name: str) -> list:
        """Tracking. Check users last result"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT first_name
            FROM results
            WHERE user_id = {user_id}
            AND task_name = '{task_name}'
            """
            data = await conn.fetch(query)
            ready_data = [task[0] for task in data]
        return ready_data

    async def register_first_result(
            self, user_id: int, task_name: str, first_result_name: str):
        """Tracking. Register a first result for user task"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            reg_query = f"""
            INSERT INTO results
            (USER_ID, TASK_NAME, FIRST_NAME)
            VALUES ({user_id}, '{task_name}', '{first_result_name}');
            """
            await conn.execute(reg_query)


class DBPayment(DBConnect):
    async def worker_quantity_check(self, user_id: int) -> int:
        """CRUD Payment. Read how many workers are allowed."""
        await DBConnect.connect(self)
        now = str(datetime.now()).split(' ')[0]
        async with self.pool.acquire() as conn:
            workers_query = f"""
                        SELECT workers_quantity
                        FROM subscribers
                        WHERE user_id = {user_id}
                        AND end_date > '{now}';"""
            data = await conn.fetchval(workers_query)
            return data

    async def is_subscriber(self, user_id: int) -> bool:
        """CRUD Payment. Read if user is subscriber or not."""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            now = str(datetime.now()).split(' ')[0]
            check_query = f"""
                    SELECT COUNT(*)
                    FROM subscribers
                    WHERE user_id = {user_id}
                    AND end_date > '{now}';"""
            data = await conn.fetchval(check_query)
            return False if data == 0 else True

    async def create_new_subscriber(
            self, user_id: int, now, end, worker_quantity: dict) -> None:
        """CRUD Payment. Create a subscriber."""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            reg_query = f"""
                    INSERT INTO subscribers
                    (user_id, purchase_date, end_date, workers_quantity)
                    VALUES ({user_id}, '{now}', '{end}', {worker_quantity});
                    """
            await conn.execute(reg_query)


class DBCommands(DBTracking, DBPayment):
    async def get_active_users(self) -> list:
        """CRUD operation. Read all active users"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            query = """
            SELECT user_id
            FROM users
            WHERE is_tracking = 1
            """
            data = await conn.fetch(query)
            ready_data = [user_id[0] for user_id in data]
            return ready_data

    async def is_alive(self, user_id: int):
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT is_tracking
            FROM users
            WHERE user_id = {user_id}
            """
            return await conn.fetchval(query)

    async def create_user(self, user_id: int) -> bool:
        """CRUD operation. Create a user."""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
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
                return is_registered

    async def delete_task(self, user_id: int, task_name: str) -> str:
        """CRUD operation. Deleting a task"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
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
            if resp[-1] == '0':
                return f'Неправильное имя задачи {task_name}'
            else:
                return f'Успешное удаление {task_name}'

    async def create_task(self, user_id: int, name: str, url: str) -> None:
        """CRUD operation. Creating a task"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            insert_query = f"""
            INSERT INTO workers
            (USER_ID, TASK_NAME, TASK_URL)
            VALUES ({user_id}, {name}, {url});
            """
            await conn.execute(insert_query)

    async def read_tasks(self, user_id: int) -> dict:
        """CRUD operation. Reading a users tasks"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            read_query = f"""
            SELECT TASK_NAME, TASK_URL
            FROM workers
            WHERE USER_ID = {user_id}"""
            data = await conn.fetch(read_query)
            result = {row[0]: row[1] for row in data}
        return result

    async def read_user_task(self, user_id: int) -> str:
        """CRUD operation. Reading a users tasks names"""
        await DBConnect.connect(self)
        async with self.pool.acquire() as conn:
            check_query = f"""
            SELECT TASK_NAME, TASK_URL
            FROM workers
            WHERE USER_ID = {user_id}"""
            data = await conn.fetch(check_query)
            result = [
                f"{name[0]} || {name[1]}"
                for name in data
            ]
        return ', \n'.join(result)
