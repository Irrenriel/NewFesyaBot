from aiogram.types import Message

from src.content import LOC_HELP_TEXT


async def loc_help(mes: Message):
    await mes.answer(LOC_HELP_TEXT)