from logging import info

from aiogram import Dispatcher

from .main_handlers import register_main_handlers
from .admin_handlers import register_admin_handlers
from .alliance_handlers import register_alliance_handlers
from .location_handlers import register_location_handlers
from .at_guild_handlers import register_at_guild_handlers
from .workbench_handlers import register_workbench_handlers


async def run_handlers(dp: Dispatcher):
    info('▻ Installing a handlers...')

    await register_main_handlers(dp)
    info('▻ MAIN handlers was successful installed!')

    await register_admin_handlers(dp)
    info('▻ ADMIN handlers was successful installed!')

    await register_at_guild_handlers(dp)
    info('▻ AT GUILD handlers was successful installed!')

    await register_alliance_handlers(dp)
    info('▻ ALLIANCE handlers was successful installed!')

    await register_location_handlers(dp)
    info('▻ LOCATION handlers was successful installed!')

    await register_workbench_handlers(dp)
    info('▻ WORKBENCH handlers was successful installed!')
