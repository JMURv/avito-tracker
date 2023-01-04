from avito_tracker.data_base.config import DSN
from datetime import datetime
import asyncpg
from asyncpg import exceptions


class DBCommands:

    def __init__(self):
        self.dsn = DSN
        self.pool = None

    async def worker_quantity_check(self, user_id: int) -> int:
        """CRUD Payment. Read how many workers are allowed."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            workers_query = f"""
                SELECT workers_quantity
                FROM subscribers
                WHERE user_id = {user_id};"""
            data = await conn.fetchval(workers_query)
            return data

    async def check_for_subscription(self, user_id: int) -> bool:
        """CRUD Payment. Read if user is subscriber or not."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            now = str(datetime.now()).split(' ')[0]
            check_query = f"""
            SELECT COUNT(*)
            FROM subscribers
            WHERE user_id = {user_id}
            AND end_date > '{now}';"""
            data = await conn.fetchval(check_query)
            return False if data == 0 else True

    async def register_new_subscriber(
            self, user_id: int, now: str, end: str, data: dict) -> None:
        """CRUD Payment. Create a subscriber."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            worker_quantity = data.get('worker_quantity')
            reg_query = f"""
            INSERT INTO subscribers
            (user_id, purchase_date, end_date, workers_quantity)
            VALUES ({user_id}, '{now}', '{end}', {worker_quantity});
            """
            await conn.execute(reg_query)

    async def get_active_users(self) -> list:
        """CRUD operation. Read all active users"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            query = """
            SELECT user_id
            FROM users
            WHERE is_tracking = 1
            """
            data = await conn.fetch(query)
            ready_data = [user_id[0] for user_id in data]
            return ready_data

    async def enable_track(self, user_id: int) -> None:
        """Tracking. Enable it."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            update_query = f"""
                UPDATE users
                SET is_tracking = 1
                WHERE user_id = {user_id};
                """
            await conn.execute(update_query)

    async def disable_track(self, user_id: int) -> None:
        """Tracking. Disable it and remove results."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
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

    async def is_tracking_now(self, user_id: int):
        """Tracking. Check if tracking is active."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT is_tracking
            FROM users
            WHERE user_id = {user_id};"""
            data = await conn.fetchval(query)
        return data

    async def register_user(self, user_id: int) -> bool:
        """CRUD operation. Create a user."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
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

    async def check_if_exists(self, user_id: int) -> bool:
        """Tracking. Read users result if it exists"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT *
            FROM results
            WHERE user_id = {user_id}
            """
            data = await conn.fetch(query)
            return True if len(data) > 0 else False

    async def update_result(self, user_id: int, task_name: str, new_name: str) -> None:
        """Tracking. Update last result."""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            update_query = f"""
            UPDATE results
            SET first_name = '{new_name}'
            WHERE user_id = {user_id}
            AND task_name = '{task_name}'
            """
            await conn.execute(update_query)

    async def read_result(self, user_id: int, task_name: str) -> None:
        """Tracking. Check users last result"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            query = f"""
            SELECT first_name
            FROM results
            WHERE user_id = {user_id}
            AND task_name = '{task_name}'
            """
            data = await conn.fetchval(query)
        return data

    async def register_first_result(
            self, user_id: int, task_name: str, fres_name: str) -> None:
        """Tracking. Register a first result for user task"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            reg_query = f"""
            INSERT INTO results
            (USER_ID, TASK_NAME, FIRST_NAME)
            VALUES ({user_id}, '{task_name}', '{fres_name}');
            """
            await conn.execute(reg_query)

    async def delete_data(self, user_id: int, worker_name: str) -> str:
        """CRUD operation. Deleting a task"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            delete_query = f"""
            DELETE FROM workers
            WHERE USER_ID = {user_id}
            AND TASK_NAME = '{worker_name}';"""
            resp = await conn.execute(delete_query)
            if resp[-1] == '0':
                return f'Неправильное имя задачи {worker_name}'
            else:
                return f'Успешное удаление {worker_name}'

    async def insert_values(self, user_id: int, name: str, url: str) -> None:
        """CRUD operation. Creating a task"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            insert_query = f"""
            INSERT INTO workers
            (USER_ID, TASK_NAME, TASK_URL)
            VALUES ({user_id}, {name}, {url});
            """
            await conn.execute(insert_query)

    async def read_data(self, user_id: int) -> dict:
        """CRUD operation. Reading a users tasks"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            read_query = f"""
            SELECT TASK_NAME, TASK_URL
            FROM workers
            WHERE USER_ID = {user_id}"""
            data = await conn.fetch(read_query)
            result = {row[0]: row[1] for row in data}
        return result

    async def check_workers(self, user_id: int) -> str:
        """CRUD operation. Reading a users tasks names"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        async with self.pool.acquire() as conn:
            check_query = f"""
            SELECT TASK_NAME
            FROM workers
            WHERE USER_ID = {user_id}"""
            data = await conn.fetch(check_query)
            result = [name[0] for name in data]
        return ', '.join(result)
