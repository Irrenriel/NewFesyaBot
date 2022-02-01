from logging import info

from aiogram import Dispatcher

from .main_handlers import register_main_handlers
from .admin_handlers import register_admin_handlers
from .alliance_handlers import register_alliance_handlers
from .location_handlers import register_location_handlers


async def run_handlers(dp: Dispatcher):
    info('▻ Installing a handlers...')

    await register_main_handlers(dp)
    info('▻ MAIN handlers was successful installed!')

    await register_admin_handlers(dp)
    info('▻ ADMIN handlers was successful installed!')

    await register_alliance_handlers(dp)
    info('▻ ALLIANCE handlers was successful installed!')

    await register_location_handlers(dp)
    info('▻ LOCATION handlers was successful installed!')
