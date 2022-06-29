import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import config
from resources.tools import database, telethon, schedulers
from resources.tools.cw3_api.cw3_api_class import AIOCW3_API
from resources.tools.cw3_api.cw3_api_func import shops_formatter


# Loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# MemoryStorage
storage = MemoryStorage()


# Bots
bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=config.PARSE_MODE)

# Dispatchers
dp = Dispatcher(bot, storage=storage, loop=loop)


# Database
db = database.PostgreSQLDatabase(*config.POSTGRES_DB)


# Telethon client
client = telethon.TelethonConversator(*config.TELETHON_VARS, loop=loop)

# Scheduler
scheduler = schedulers.MyScheduler(loop)

# CW3 API
cw3_api = AIOCW3_API(loop, db, callbacks={'cw3-yellow_pages': shops_formatter})
