from aiogram import executor, Dispatcher

from resources.models import dp, loop, db
from src.content import Castles
from src.content.cashes import users
from src import handlers


async def startup_func(dp: Dispatcher):
    # Connecting to databases
    con = await db.connect()
    if not con:
        raise Exception('Can not connect to Database')

    # Cashes
    # UsersCash uploading
    users_result = await db.fetch('SELECT * FROM users')
    await users.update(users_result)

    result = await users.select_castle(Castles.SKALA)
    print('Result:', result)

    print('<- <- <- Bot is working! -> -> ->')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=startup_func)