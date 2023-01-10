import asyncio
from scripts.uninstall_db import uninstall_db
from scripts.install_db import install_db


async def reinstall_db():
    await uninstall_db()
    await install_db()


if __name__ == '__main__':
    asyncio.run(reinstall_db())
