from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, ChatTypeFilter, Text

from config import config
from resources.tools.cfilters import IsUser


async def register_workbench_handlers(dp: Dispatcher):
    # /start
    dp.register_message_handler(
        start,
        Text('⚒Мастерская'), ChatTypeFilter('private'), IsUser(is_registered=True, is_id=config.WORKBENCH_MEMBERS_IDS)
    )