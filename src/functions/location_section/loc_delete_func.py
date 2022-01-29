import asyncio

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import DELETE_LOC_NTF
from src.content.consts.main_resources import ChatInfo


async def loc_del(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_del [код локации]')
        return

    loc = await db.fetch('SELECT * FROM loc WHERE code = $1 and exist = True', [code], one_row=True)
    if not loc:
        await mes.answer('[❌] Невозможно. Такой локации нет в базе.')
        return

    await db.execute(
        'UPDATE loc SET exist = False, death_time = LOCALTIMESTAMP WHERE code = $1', [code]
    )

    # Notifications
    chats = [ChatInfo(**c) for c in await db.fetch(DELETE_LOC_NTF)]

    if chats:
        answer = f'<b>[📣] Локация с кодом <code>{code}</code> была удалена!</b>'

        for chat in chats:
            try:
                await asyncio.sleep(0.3)
                await mes.bot.send_message(chat.id, answer)

            except Exception:
                pass

    await mes.answer(f'<b>[✅] Выполнено!</b>')


async def loc_resurrect(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_resurrect [код локации]')
        return

    loc = await db.fetch('SELECT * FROM loc WHERE code = $1 and exist = False', [code], one_row=True)
    if not loc:
        await mes.answer('[❌] Невозможно. Такой локации нет в среди мёртвых.')
        return

    await db.execute(
        'UPDATE loc SET exist = True, death_time = found_time WHERE code = $1', [code]
    )

    # Notifications
    chats = [ChatInfo(**c) for c in await db.fetch(DELETE_LOC_NTF)]

    if chats:
        answer = f'<b>[📣] Локация с кодом <code>{code}</code> ожила!</b>'

        for chat in chats:
            try:
                await asyncio.sleep(0.3)
                await mes.bot.send_message(chat.id, answer)

            except Exception:
                pass

    await mes.answer(f'<b>[✅] Выполнено!</b>')
