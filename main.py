from aiogram import executor, Dispatcher

from resources.models import dp, loop, db
from resources.tools.middleware import Middleware
from src.content import users, MAIN_REQ, adv_users, ADV_MAIN_REQ, banned_users, BANNED_MAIN_REQ
from src import handlers


async def startup_func(dp: Dispatcher):
    print('= = = Starting a bot! = = =')
    # Skip updates
    await dp.skip_updates()
    print('▻ Updates skipped!')

    # Connecting to databases
    con = await db.connect()
    if not con:
        raise Exception('Can not connect to Database')
    print('▻ Database connected!')

    # Cashes
    await users.update(await db.fetch(MAIN_REQ))
    print('▻ UsersCash is running!')

    await adv_users.update(await db.fetch(ADV_MAIN_REQ))
    print('▻ AdvUsersCash is running!')

    await banned_users.update(await db.fetch(BANNED_MAIN_REQ))
    print('▻ BannedUsersCash is running!')

    dp.middleware.setup(Middleware(db, users, adv_users))
    print('▻ Middleware is setup!')

    print('= = = Bot is working! = = =')

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, on_startup=startup_func)
