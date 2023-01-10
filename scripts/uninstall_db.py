import asyncio
import asyncpg
from avito_tracker.data_base.config import DSN


async def uninstall_db():
    conn = await asyncpg.connect(DSN)
    command = """DELETE TABLE users, workers, results, subscribers CASCADE;"""
    await conn.execute(command)


if __name__ == '__main__':
    asyncio.run(uninstall_db())
