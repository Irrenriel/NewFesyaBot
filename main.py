from logging import info
from sys import argv

from aiogram import executor, Dispatcher

import config
from resources.models import dp, loop, db, client
from resources.tools import bot_logging
from resources.tools.middleware import Middleware
from src.content import users, MAIN_REQ, adv_users, ADV_MAIN_REQ, banned_users, BANNED_MAIN_REQ
from src import handlers


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')

    # Skip updates
    await dp.skip_updates()
    info('▻ Updates skipped!')

    # Connecting to databases
    con = await db.connect()
    if not con:
        raise Exception('Can not connect to Database')
    info('▻ Database connected!')

    # Cashes
    await users.update(await db.fetch(MAIN_REQ))
    info('▻ UsersCash is running!')

    await adv_users.update(await db.fetch(ADV_MAIN_REQ))
    info('▻ AdvUsersCash is running!')

    await banned_users.update(await db.fetch(BANNED_MAIN_REQ))
    info('▻ BannedUsersCash is running!')

    dp.middleware.setup(Middleware(db, users, adv_users))
    info('▻ Middleware is setup!')

    # Telethon
    if client._client.is_connected():
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is running!')

    else:
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is not running!')

    info('= = = Bot is working! = = =')

if __name__ == '__main__':
    # Set Logging
    debug = "--debug" in argv
    bot_logging.set_logging(debug)

    executor.start_polling(dp, loop=loop, on_startup=startup_func)
