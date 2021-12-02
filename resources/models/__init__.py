import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN_1, BOT_TOKEN_2, PARSE_MODE

# Here you can create tool instances if needed.

# Loop
loop = asyncio.get_event_loop()

# MemoryStorage
storage = MemoryStorage()


# Bots
bot_1 = Bot(token=BOT_TOKEN_1, loop=loop, parse_mode=PARSE_MODE)
bot_2 = Bot(token=BOT_TOKEN_2, loop=loop, parse_mode=PARSE_MODE)

# Dispatchers
dp_1 = Dispatcher(bot_1, storage=storage, loop=loop)
dp_2 = Dispatcher(bot_2, storage=storage, loop=loop)