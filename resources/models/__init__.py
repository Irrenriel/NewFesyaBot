import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, PARSE_MODE

# Here you can create tool instances if needed.

# Loop
loop = asyncio.get_event_loop()

# MemoryStorage
storage = MemoryStorage()


# Bot
bot = Bot(token=BOT_TOKEN, loop=loop, parse_mode=PARSE_MODE)

# Dispatcher
dp = Dispatcher(bot, storage=storage, loop=loop)