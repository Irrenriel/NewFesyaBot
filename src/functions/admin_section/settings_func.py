import asyncio
from logging import info

from aiogram.types import CallbackQuery, Message


# Cancel Callback
from aiogram.utils.exceptions import MessageCantBeDeleted

from resources.tools.database import PostgreSQLDatabase
from src.content import UsersCash, MAIN_REQ, ADV_MAIN_REQ, BANNED_MAIN_REQ, AdvUsersCash, BannedUsersCash


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


# Update Cashes
async def update_cashes(mes: Message, db: PostgreSQLDatabase):
    cashes = ['USERS', 'ADV_USERS', 'BANNED']

    cash_name = (mes.get_args()).upper()
    if not cash_name or cash_name not in cashes:
        await mes.answer(f'Available cashes: {", ".join([f"<code>{cash}</code>" for cash in cashes])}')
        return

    if cash_name == 'USERS':
        await UsersCash.update(await db.fetch(MAIN_REQ))
        info('▻ UsersCash was updated!')

    if cash_name == 'ADV_USERS':
        await AdvUsersCash.update(await db.fetch(ADV_MAIN_REQ))
        info('▻ AdvUsersCash was updated!')

    if cash_name == 'BANNED':
        await BannedUsersCash.update(await db.fetch(BANNED_MAIN_REQ))
        info('▻ BannedUsersCash was updated !')

    await mes.answer(f'{cash_name} cash was updated!')