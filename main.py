from logging import info

from aiogram import executor, Dispatcher
from telethon import TelegramClient

from config import config
from resources.models import dp, loop, db, client
from resources.tools import bot_logging
from resources.tools.middleware import installing_middlewares
from src.content import installing_cashes
from src.handlers import run_handlers


async def telethon_connect_check(app: TelegramClient):
    if app.is_connected():
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is running!')

        for i in ['@ChatWarsBot', '@ChatWarsDigest']:
            try:
                x = await app.get_entity(i)

            except Exception:
                x = None

            info(f'▻ {i} entity is founded!' if x else f'▻ {i} entity is not founded!')

    else:
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is not running!')


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')
    info(f'Current version: {config.CURRENT_VERSION}')

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

    info('= = = = = = = = =')

    # Middlewares
    await installing_middlewares(dp, db)

    info('= = = Bot is working! = = =')

if __name__ == '__main__':
    # Set Logging
    bot_logging.set_logging(config.debug)

    executor.start_polling(dp, loop=loop, on_startup=startup_func)
