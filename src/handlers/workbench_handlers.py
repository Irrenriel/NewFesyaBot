from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, ChatTypeFilter, Text, RegexpCommandsFilter

from config import config
from resources.tools.cfilters import IsUser
from resources.tools.states import StateOn
from src.functions import craft, crafting_item_func


async def register_workbench_handlers(dp: Dispatcher):
    # ⚒Мастерская
    dp.register_message_handler(
        craft,
        Text('⚒Мастерская'), ChatTypeFilter('private'), IsUser(is_registered=True, is_id=config.WORKBENCH_MEMBERS_IDS)
        # State: None -> StateOn.WorkBenchActive
    )

    # /c_id
    dp.register_message_handler(
        crafting_item_func,
        RegexpCommandsFilter(regexp_commands=['c_.+']), ChatTypeFilter('private'),
        IsUser(is_registered=True, is_id=config.WORKBENCH_MEMBERS_IDS), state=StateOn.WorkBenchActive
    )