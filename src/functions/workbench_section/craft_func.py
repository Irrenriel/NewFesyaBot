from aiogram.types import Message

from resources.tools.states import StateOn
from src.content.texts.workbench_txt import CRAFT_TEXT


async def craft(mes: Message):
    await mes.answer(CRAFT_TEXT)
    await StateOn.WorkBenchActive.set()
