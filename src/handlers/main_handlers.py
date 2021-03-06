from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import RegexpCommandsFilter

from config import config

from resources.tools.cfilters import Command, IsUser, ChatTypeFilter, Text, IsForward, IsBotAddedToChat
from resources.tools.states import StateOn
from src.content import Roles
from src.functions import start, hero_insert, start_new, new_chat_found, settings, top1, top2, settings_v, ws_shops, \
    ws_owners


async def register_main_handlers(dp: Dispatcher):
    """
    Registration MAIN handlers.
    :param dp: aiogram Dispatcher
    :return:
    """
    # /start
    dp.register_message_handler(
        start,
        Command('start'), ChatTypeFilter('private'), IsUser(is_registered=True), state='*'
    )

    # 🗳Меню, Вернуться↩
    dp.register_message_handler(
        start,
        Text(['🗳Меню', 'Вернуться↩']), ChatTypeFilter('private'), IsUser(is_registered=True), state='*'
    )

    # /start (New User)
    dp.register_message_handler(
        start_new,
        Command('start'), ChatTypeFilter('private'), IsUser(is_registered=False), state='*'
        # State: None -> StateOn.Registration
    )

    # From CW /hero Inputer For Registration
    dp.register_message_handler(
        hero_insert,
        ChatTypeFilter('private'), state=StateOn.Registration
        # State: StateOn.Registration -> None
    )

    # From CW /hero Inputer For Update
    dp.register_message_handler(
        hero_insert,
        Text(contains="🎉Достижения: /ach"), IsForward(config.CW_BOT_ID), IsUser(is_registered=True)
    )

    # Adding bot to a new chat
    dp.register_message_handler(
        new_chat_found,
        IsBotAddedToChat(), content_types='new_chat_members'
    )

    # /settings
    dp.register_message_handler(
        settings,
        Command('settings'), ChatTypeFilter(types.ChatType.GROUP),
        IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER])
    )

    dp.register_message_handler(
        settings,
        Command('settings'), ChatTypeFilter(types.ChatType.SUPERGROUP),
        IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER])
    )

    dp.register_callback_query_handler(
        settings_v,
        Text(startswith=['nln:', 'dln:', 'brf:', 'brfm:']),
        IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER])
    )

    # /top1
    dp.register_message_handler(
        top1,
        Command('top1')
    )

    # /top2
    dp.register_message_handler(
        top2,
        Command('top2')
    )

    # /ws
    dp.register_message_handler(
        ws_shops,
        Command('ws'),
        state=[None, StateOn.WorkBenchActive]
    )

    # /ws_link
    dp.register_message_handler(
        ws_owners,
        RegexpCommandsFilter(regexp_commands=['ws_(.*)']),
        state=[None, StateOn.WorkBenchActive]
    )
