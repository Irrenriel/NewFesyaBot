from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import HELP_NEW_CHAT_ID_TEXT, SETTINGS_GET_CHAT
from src.content.consts.main_resources import ChatInfo


async def new_chat_found(mes: Message, db: PostgreSQLDatabase):
    if await db.fetch('SELECT * FROM chats WHERE id = $1', [mes.chat.id], one_row=True):
        return

    await db.execute('INSERT INTO chats (id) VALUES ($1)', [mes.chat.id])
    await mes.answer(HELP_NEW_CHAT_ID_TEXT)


async def settings(mes: Message, db: PostgreSQLDatabase):
    req = await db.fetch(SETTINGS_GET_CHAT, [mes.chat.id], one_row=True)

    if not req:
        await db.execute('INSERT INTO chats (id) VALUES ($1)', [mes.chat.id])
        req = await db.fetch(SETTINGS_GET_CHAT, [mes.chat.id], one_row=True)

    chat = ChatInfo(**req)
