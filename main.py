import sys
from logging import info

from aiogram import executor, Dispatcher

from config import config
from resources.models import dp, loop, db, client, scheduler
from resources.tools import bot_logging
from resources.tools.middleware import installing_middlewares
from resources.tools.telethon import telethon_connect_check
from src.content import installing_cashes, installing_schedulers
from src.handlers import run_handlers


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')
    info(f'Current version: {config.APP_VERSION}')

    # Skip updates
    await dp.skip_updates()

    # Handlers
    await run_handlers(dp)

    info('= = = = = = = = =')

    # Connecting to databases
    await db.connect()

    # Telethon
    await telethon_connect_check(client.client)

    info('= = = = = = = = =')

    # Cashes
    await installing_cashes(db)

    # Schedulers
    await installing_schedulers(db, scheduler, loop)

    info('= = = = = = = = =')

    # Middlewares
    await installing_middlewares(dp, db)

    info('= = = Bot is working! = = =')

if __name__ == '__main__':
    # Process Name (for Linux)
    if sys.platform == 'linux':
        import ctypes

        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, 'F', 0, 0, 0)

    # Set Logging
    bot_logging.set_logging(config.debug)

    client.client.start()
    executor.start_polling(dp, loop=loop, on_startup=startup_func)
