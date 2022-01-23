from logging import StreamHandler, INFO, WARNING, basicConfig, info, Filter
from logging.handlers import RotatingFileHandler
from sys import stdout, argv

from aiogram import executor, Dispatcher

import config
from resources.models import dp, loop, db, client
from resources.tools.middleware import Middleware
from src.content import users, MAIN_REQ, adv_users, ADV_MAIN_REQ, banned_users, BANNED_MAIN_REQ
from src import handlers


async def set_logging(debug: bool):
    class MyFilter(Filter):
        def __init__(self, level, name=''):
            self.__level = level
            super(MyFilter, self).__init__(name)

        def filter(self, log_record):
            return log_record.levelno <= self.__level

    console = StreamHandler(stdout)
    console_lvl = INFO if debug else WARNING
    console.setLevel(console_lvl)
    console.addFilter(MyFilter(INFO))

    file_log = RotatingFileHandler(
        filename='logs/soft.log', mode='a', maxBytes=512_000_000, backupCount=1,
        encoding="utf-8"
    )
    file_log.setLevel(INFO)

    error = StreamHandler()
    error.setLevel(WARNING)

    basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO, handlers=[console, error, file_log]
    )


async def startup_func(dp: Dispatcher):
    info('= = = Starting a bot! = = =')
    debug = "--debug" in argv

    # Logger
    await set_logging(debug)
    info('▻ Logger is running!!')

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
    executor.start_polling(dp, loop=loop, on_startup=startup_func)
