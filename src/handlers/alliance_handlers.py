from aiogram import Dispatcher

from config import config

from resources.tools.cfilters import Command, IsUser, ChatTypeFilter, Text, IsForward
from resources.tools.states import StateOn
from src.functions import alliance_main_menu, alliance_new_reg, alliance_get_main, alliance_get_code,\
    alliance_get_roster


async def register_alliance_handlers(dp: Dispatcher):
    """
    Registration ALLIANCE handlers.
    :param dp: aiogram Dispatcher
    :return:
    """
    # 🎪Альянс
    dp.register_message_handler(
        alliance_main_menu,
        Text('🎪Альянс'), ChatTypeFilter('private'), IsUser(is_registered=True)
    )

    # New Alliance Registration
    dp.register_callback_query_handler(
        alliance_new_reg,
        Text('al:new'), ChatTypeFilter('private'), IsUser(is_registered=True)
        # State: None -> AllianceUpd.GetCode
    )

    # NewAllReg Get Code
    dp.register_message_handler(
        alliance_get_code,
        ChatTypeFilter('private'), IsUser(is_registered=True), state=StateOn.AllianceGetCode
        # State: AllianceUpd.GetCode -> AllianceUpd.GetMenu
    )

    # NewAllReg Get Menu
    dp.register_message_handler(
        alliance_get_main,
        Text(startswith='🤝'), ChatTypeFilter('private'), IsForward(config.CW_BOT_ID), IsUser(is_registered=True),
        state=StateOn.AllianceGetMenu
        # State: AllianceUpd.GetMenu -> AllianceUpd.GetRoster
    )

    # NewAllReg Get Roster
    dp.register_message_handler(
        alliance_get_roster,
        Text(startswith='📋Roster:\n'), ChatTypeFilter('private'), IsForward(config.CW_BOT_ID),
        IsUser(is_registered=True), state=StateOn.AllianceGetRoster
        # State: AllianceUpd.GetRoster -> None
    )