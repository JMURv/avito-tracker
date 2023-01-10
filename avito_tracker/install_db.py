import asyncio
import asyncpg
from avito_tracker.data_base.config import DSN


async def install_db():
    conn = await asyncpg.connect(DSN)
    commands = [
        """CREATE TABLE IF NOT EXIST users (
            user_id integer UNIQUE,
            is_tracking integer);""",

        """CREATE TABLE IF NOT EXIST workers (
            user_id REFERENCES users(user_id),
            task_name varchar(255),
            task_url varchar(255));""",

        """CREATE TABLE IF NOT EXIST results (
            user_id REFERENCES users(user_id),
            task_name varchar(255),
            first_name varchar(255));""",

        """CREATE TABLE IF NOT EXIST subscribers (
            user_id REFERENCES users(user_id),
            purchase_date date,
            end_date date,
            workers_quantity integer);"""
    ]
    for command in commands:
        try:
            await conn.execute(command)
        except Exception:
            print("Что-то пошло не так")


async def uninstall_db():
    conn = await asyncpg.connect(DSN)
    command = """DELETE TABLE users, workers, results, subscribers CASCADE;"""
    await conn.execute(command)


async def reinstall_db():
    await uninstall_db()
    await install_db()


if __name__ == '__main__':
    asyncio.run(install_db())
