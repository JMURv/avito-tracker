import asyncio
import os

import asyncpg


async def uninstall_db():
    conn = await asyncpg.connect(os.getenv("DSN"))
    command = """DROP TABLE users, workers, results, subscribers CASCADE;"""
    await conn.execute(command)


if __name__ == '__main__':
    asyncio.run(uninstall_db())
