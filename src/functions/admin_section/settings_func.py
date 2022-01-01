import asyncio

from aiogram.types import CallbackQuery, Message


# Cancel Callback
from aiogram.utils.exceptions import MessageCantBeDeleted


async def callback_cancel(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.delete()


# None Callback
async def callback_none(call: CallbackQuery):
    await call.answer()


# Delete message with notification at timer
async def delete_message_with_notification(mes: Message, m: Message, t1: int, t2: int):
    try:
        await asyncio.sleep(t1)
        await mes.delete()

    except MessageCantBeDeleted:
        pass

    try:
        await asyncio.sleep(t2)
        await m.delete()

    except MessageCantBeDeleted:
        pass