import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, PARSE_MODE, POSTGRES_DB, TELETHON_VARS
from resources.tools import database, telethon


# Loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# MemoryStorage
storage = MemoryStorage()


# Bots
bot = Bot(token=BOT_TOKEN, loop=loop, parse_mode=PARSE_MODE)

# Dispatchers
dp = Dispatcher(bot, storage=storage, loop=loop)


# Database
db = database.PostgreSQLDatabase(*POSTGRES_DB)


# Telethon client
client = telethon.TelethonConversator(*TELETHON_VARS, loop=loop)
