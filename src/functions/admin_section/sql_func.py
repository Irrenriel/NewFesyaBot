from aiogram.types import Message
import re

from asyncpg import Record

from resources.tools.database import PostgreSQLDatabase
from src.content import ADMIN_REPLY_INFO_TEXT, users, adv_users, MAIN_REQ, ADV_MAIN_REQ


# /sql
async def sql(mes: Message, db: PostgreSQLDatabase):
    parse = re.search(r'/sql (?P<mode>\d) (?P<poll>.+)', mes.text)
    if not parse or parse.group('mode') not in ['1', '2', '3']:
        await mes.answer('ValueError: Incorrect Syntax!')
        return

    mode, poll = int(parse.group('mode')), parse.group('poll')

    txt = await db_req(db, mode, poll)
    if txt is None:
        await mes.answer('ValueError: Incorrect Syntax!')
        return

    if mode == 3:
        await users.update(await db.fetch(MAIN_REQ))
        await adv_users.update(await db.fetch(ADV_MAIN_REQ))

    await mes.answer(txt)


async def db_req(db: PostgreSQLDatabase, mode: int, poll: str, limit: int = 40000):
    try:
        if mode == 1 or mode == 2:
            result = await db.fetch(poll, one_row=True if mode == 1 else False)
            if type(result) is Record:
                txt = f'<b>Result:</b>\n{dict(result.items())}'
            else:
                txt = f'<b>Result:</b>\n'
                for i, x in enumerate(result, start=1):
                    txt += f'<b>{i} — </b>{dict(x.items())}\n'

        elif mode == 3:
            await db.execute(poll)
            txt = 'Success: Done!'

        else:
            return

    except Exception:
        txt = 'Error: Incorrect Request!'

    return txt[:limit]


# /inf
async def info(mes: Message):
    mr = mes.reply_to_message

    answer = {
        'message_id': str(mr.message_id),
        'user_id': str(mr.from_user.id),
        'user_is_bot': str(mr.from_user.is_bot),
        'user_first_name': mr.from_user.first_name if mr.from_user.first_name else 'None',
        'user_last_name': mr.from_user.last_name if mr.from_user.last_name else 'None',
        'user_username': mr.from_user.username if mr.from_user.username else 'None',
        'user_language_code': mr.from_user.language_code if mr.from_user.language_code else 'None',
        'chat_id': str(mr.chat.id),
        'chat_type': mr.chat.type,
        'chat_title': mr.chat.title,
        'chat_username': mr.chat.username if mr.chat.username else 'None',
        'date': str(mr.date)
    }

    await mes.answer(ADMIN_REPLY_INFO_TEXT.format(**answer))
