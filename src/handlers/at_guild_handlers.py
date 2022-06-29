from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, RegexpCommandsFilter

from resources.tools.cfilters import IsUser
from src.functions import gold_func, open_shop_func, change_cost_func


async def register_at_guild_handlers(dp: Dispatcher):
    # /gold
    dp.register_message_handler(
        gold_func,
        Command('gold'), IsUser(is_registered=True)
    )

    # /open_shop
    dp.register_message_handler(
        open_shop_func,
        Command('open_shop'), IsUser(is_registered=True)
    )

    # /cc
    dp.register_message_handler(
        change_cost_func,
        RegexpCommandsFilter(regexp_commands=['cc_([0-9]*)']), IsUser(is_registered=True)
    )
