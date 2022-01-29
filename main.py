from logging import info

from aiogram import executor, Dispatcher

from config import config
from resources.models import dp, loop, db, client
from resources.tools import bot_logging
from resources.tools.middleware import Middleware, BanMiddleware, ThrottleMiddleware
from src.content import UsersCash, AdvUsersCash, BannedUsersCash, MAIN_REQ, ADV_MAIN_REQ, BANNED_MAIN_REQ
from src import handlers  # Do not delete this!!!


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')
    info(f'Current version: {config.CURRENT_VERSION}')

    # Skip updates
    await dp.skip_updates()
    info('▻ Updates skipped!')

    # Connecting to databases
    con = await db.connect()
    if not con:
        raise Exception('Can not connect to Database')
    info('▻ Database connected!')

    # Telethon
    if client.client.is_connected():
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is running!')

        u = '@ChatWarsBot'
        try:
            x = await client.client.get_entity(u)

        except Exception:
            x = None

        if x:
            info(f'▻ {u} entity is founded!')

        else:
            info(f'▻ {u} entity is not founded!')

    else:
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is not running!')

    info('= = = = = = = = =')

    # Cashes
    await UsersCash.update(await db.fetch(MAIN_REQ))
    info('▻ UsersCash is running!')

    await AdvUsersCash.update(await db.fetch(ADV_MAIN_REQ))
    info('▻ AdvUsersCash is running!')

    await BannedUsersCash.update(await db.fetch(BANNED_MAIN_REQ))
    info('▻ BannedUsersCash is running!')

    info('= = = = = = = = =')

    dp.middleware.setup(BanMiddleware(db))
    info('▻ BanMiddleware is setup!')

    dp.middleware.setup(ThrottleMiddleware())
    info('▻ ThrottleMiddleware is setup!')

    dp.middleware.setup(Middleware(db))
    info('▻ Middleware is setup!')

    info('= = = Bot is working! = = =')

if __name__ == '__main__':
    # Set Logging
    bot_logging.set_logging(config.debug)

    executor.start_polling(dp, loop=loop, on_startup=startup_func)
