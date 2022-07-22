import asyncio
import random
import re

from aiogram.types import Message

from resources.models import client
from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from resources.tools.telethon import TelethonQueue
from src.content import CraftData
from src.content.texts.workbench_txt import CRAFT_TEXT


async def craft(mes: Message):
    await mes.answer(CRAFT_TEXT)
    await StateOn.WorkBenchActive.set()


async def crafting_item_func(mes: Message, db: PostgreSQLDatabase):
    if not await check_queue(mes):
        return

    with TelethonQueue() as tq:
        answer = await client.conversation(mes.text, float(str(random.uniform(1, 3))[0:4]))

    if not answer:
        await mes.answer('<b>[❌] Не удалось получить ответа от CW бота!</b>')
        return

    if 'Не хватает материалов для крафта' in answer:
        f_list = {k: int(v) for v, k in re.findall(r'(\d+) x ([^\n$]+)', answer)}
        res = await db.fetch_orm(
            CraftData, 'SELECT cid, name FROM craft_ids WHERE name = any($1::text[])', [list(f_list.keys())]
        )

        # !!!

    else:
        await mes.answer(f'<b>CW:</b>\n{answer.message}')


async def guild_stock_refresh(mes: Message):
    pass


async def check_queue(mes: Message):
    status = TelethonQueue.get_status()
    temp_message = None
    tries = 0

    while not status and tries < 3:
        if not temp_message:
            temp_message = await mes.answer('<b>[❌] Аккаунт занят. Подождите!</b>')

        await asyncio.sleep(2)

        status = TelethonQueue.get_status()
        tries += 1

    else:
        if temp_message and status:
            await temp_message.delete()

        elif temp_message and not status:
            await temp_message.edit_text('<b>[❌] Аккаунт занят чем-то долгим. Попробуйте позже!</b>')

        return status
