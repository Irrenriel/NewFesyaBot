from aiogram import executor, Dispatcher

from resources.models import dp, loop, db
from resources.tools.cashes import UserData
from src import handlers


async def startup_func(dp: Dispatcher):
    con = await db.connect()
    if not con:
        raise Exception('Can not connect to Database')

    result = await db.fetch('SELECT * FROM users', one_row=True)
    print('Result:', UserData(**result))
    print('<- <- <- Bot is working! -> -> ->')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=startup_func)