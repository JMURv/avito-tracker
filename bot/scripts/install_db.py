import asyncio
import asyncpg
import os


async def install_db():
    conn = await asyncpg.connect(os.getenv("DSN"))
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
        user_id integer UNIQUE,
        is_tracking integer);
        """,
        """
        CREATE TABLE IF NOT EXISTS workers (
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        task_name varchar(255),
        task_url varchar(255));
        """,
        """
        CREATE TABLE IF NOT EXISTS results (
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        task_name varchar(255),
        first_name varchar(255));
        """,
        """
        CREATE TABLE IF NOT EXISTS subscribers (
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        purchase_date date,
        end_date date,
        workers_quantity integer);
        """

    ]
    for command in commands:
        try:
            await conn.execute(command)
        except Exception as error:
            print(f"Ошибка: {error}")
            pass


if __name__ == '__main__':
    asyncio.run(install_db())
