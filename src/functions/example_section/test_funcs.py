from aiogram.types import Message


async def test(mes: Message):
    await mes.answer('Hello world')