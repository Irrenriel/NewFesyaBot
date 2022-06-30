from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, RegexpCommandsFilter, Text

from resources.tools.cfilters import IsUser
from src.content import Roles
from src.functions import gold_func, open_shop_func, change_cost_func, create_donate, update_donate, pay_donate


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

    # /create_donate, создать сбор суммы
    dp.register_message_handler(
        create_donate,
        RegexpCommandsFilter(regexp_commands=['create_donate ([0-9]*)']), IsUser(
            is_registered=True, has_roles=[Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER, Roles.ADMIN]
        )
    )

    # /cd, создать сбор суммы
    dp.register_message_handler(
        create_donate,
        RegexpCommandsFilter(regexp_commands=['cd ([0-9]*)']), IsUser(
            is_registered=True, has_roles=[Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER, Roles.ADMIN]
        )
    )

    # Обновить сборы суммы
    dp.register_callback_query_handler(
        update_donate,
        Text('updDonate'), IsUser(
            is_registered=True, has_roles=[Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER, Roles.ADMIN]
        )
    )

    # Оплатить сбор суммы
    dp.register_callback_query_handler(
        pay_donate,
        Text('doneDonate'), IsUser(
            is_registered=True, has_roles=[Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER, Roles.ADMIN]
        )
    )
