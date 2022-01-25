from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import HELP_NEW_CHAT_ID_TEXT


async def new_chat_found(mes: Message, db: PostgreSQLDatabase):
    if await db.fetch('SELECT * FROM chats WHERE id = $1', [mes.chat.id], one_row=True):
        return

    await db.execute('INSERT INTO chats (id) VALUES ($1)', [mes.chat.id])
    await mes.answer(HELP_NEW_CHAT_ID_TEXT)


async def settings(mes: Message, db: PostgreSQLDatabase):
    if not await db.fetch('SELECT * FROM chats WHERE id = $1', [mes.chat.id]):
        await mes.answer('Данного чата нет в базе. Пригласите бота по новой в чат или обратитесь к @Irrenriel.')
        return
