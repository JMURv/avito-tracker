import sys
import asyncio
from telegram import bot_start
from parsing import start_tracking


def main():
    loop = asyncio.new_event_loop()
    try:
        loop.create_task(bot_start())
        loop.create_task(start_tracking())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
