import asyncio
from logging import info

from aiogram import executor, Dispatcher

from config import config
from resources.models import dp, loop, db, client
from resources.tools import bot_logging
from resources.tools.middleware import installing_middlewares
from resources.tools.telethon import telethon_connect_check
from src.content import installing_cashes
from src.handlers import run_handlers


async def test():
    pass
    # ent = await client.client.get_entity('rybar')
    #
    # messages = await client.client.get_messages(ent, None, min_id=33264, max_id=33280)
    # await asyncio.sleep(2)
    #
    # pool = {}
    # media_group = None
    #
    # u = await client.client.get_entity('Levinfled')
    # await asyncio.sleep(2)
    #
    # for message in messages:
    #     if message.grouped_id:
    #         pool.setdefault(message.grouped_id, []).append(message)
    #
    #         if not media_group:
    #             media_group = message.grouped_id
    #
    #         elif media_group and media_group != message.grouped_id:
    #             await client.client.forward_messages(u, messages=pool.pop(media_group))
    #             media_group = None
    #
    #     else:
    #         if media_group:
    #             await client.client.forward_messages(u, messages=pool.pop(media_group))
    #             media_group = None
    #
    #         else:
    #             await client.client.forward_messages(u, message)
    #
    #         await asyncio.sleep(2)
    #
    # else:
    #     if pool:
    #         await client.client.forward_messages(u, messages=pool.pop(media_group))


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

    await test()

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
