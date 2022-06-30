import asyncio
import random
import re
from logging import info
from typing import Union, List

from telethon import TelegramClient

from config import config


class TelethonConversator:
    _con = None
    _queue = []
    _work = False

    # Settings
    _sleep = 2
    _req = 0
    _max_req = 2

    def __init__(self, SESSION_NAME: str, API_ID: int, API_HASH: str, loop):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH, loop=loop)
        self.client.start()

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def send_message(self, chat_id: Union[str, int], text: str, sleep: Union[int, float] = 0):
        await self.connect()

        if sleep:
            await asyncio.sleep(sleep)
        m = await self.client.send_message(chat_id, text)

        await self.disconnect()
        return m

    async def _action(self, text, sleep: Union[int, float] = 0, pattern=None):
        if sleep:
            await asyncio.sleep(sleep)

        await self._con.send_message(text)
        answer = (await self._con.get_response()).message

        if pattern is None:
            self._req = 0
            return answer

        parse = re.search(pattern, answer)
        if parse is None:
            # print("NON PATTERN. SLEEP:", self.sleep, "sec.")
            if self._req >= self._max_req:
                return False
            self._req += 1
            await asyncio.sleep(self._sleep)
            return await self._action(text, sleep, pattern)

        return parse

    async def conversation(self, text: Union[str, List[str]], sleep: Union[int, float] = 0, pattern=None):
        await self.connect()
        async with self.client.conversation(config.CW_BOT_ID, total_timeout=9999, timeout=5) as self._con:
            if isinstance(text, str):
                x = await self._action(text, sleep, pattern)
            else:
                x = [(await self._action(mess, sleep, pattern)) for mess in text]
        await self.disconnect()
        return x

    async def l_check_method(self, locations: Union[str, List[str]]):
        error = "Strange fog is so dense that you can't reach this place."
        pool_to_delete = []

        await self.connect()
        async with self.client.conversation(config.CW_BOT_ID, total_timeout=9999, timeout=5) as self._con:
            for loc in locations:
                if loc.startswith('NoneCode'):
                    continue

                answer = await self._action(f'/ga_atk_{loc}', round(random.uniform(1, 3), 2))
                if answer.startswith('Ветер завывает по окрестным лугам'):
                    await self.disconnect()
                    return '<b>[⚜️] Идёт битва! Попробуйте позже.</b>'

                elif answer == 'Ты сейчас занят другим приключением. Попробуй позже.':
                    await self.disconnect()
                    return '<b>[⚜️] В данный момент проверить невозможно! Попробуйте позже.</b>'

                elif answer == error:
                    answer2 = await self._action(f'/ga_def_{loc}', round(random.uniform(1, 3), 2))
                    if answer2 == error:
                        pool_to_delete.append(loc)

        await self.disconnect()
        return pool_to_delete

    async def shop_gold_method(self):
        cmds = ['/ws_MYdnt', '/ws_MYdnt_stand']
        result = {}

        await self.connect()
        async with self.client.conversation(config.CW_BOT_ID, total_timeout=9999, timeout=5) as self._con:
            for i, cmd in enumerate(cmds):
                await self._con.send_message(cmd)
                result[cmd] = (await self._con.get_response()).message

                if not i:  # Only for 2 elements
                    await asyncio.sleep(float(str(random.uniform(1, 3))[0:4]))

        await self.disconnect()
        return result


async def telethon_connect_check(client: TelegramClient):
    if client.is_connected():
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is running!')

        for i in ['@ChatWarsBot', '@ChatWarsDigest']:
            try:
                x = await client.get_entity(i)

            except Exception:
                x = None

            info(f'▻ {i} entity is founded!' if x else f'▻ {i} entity is not founded!')

    else:
        info(f'▻ Telethon client with session "{config.SESSION_NAME}" is not running!')