import asyncio

from aiogram.types import Message

from config import config
from resources.models import client
from resources.tools.database import PostgreSQLDatabase
from src.content import UserData, Roles, LOC_CHECK_SELECT_DELETED_REQ, LocInfoData, GET_LOC_TYPE_EMOJI, LocTypes, \
    MARK_AS_DEAD_LOCATIONS, DELETE_LOC_NTF
from src.content.consts.main_resources import ChatInfo
from src.functions.admin_section.settings_func import delete_message_with_notification


async def loc_check(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.role != Roles.ADMIN:
        r = 'SELECT data_bool FROM settings WHERE var = $1'

        l_check_upd = await db.fetch(r, ['l_check_upd'], one_row=True)
        if not l_check_upd.get('data_bool'):
            m = await mes.answer('<b>[❌] Не доступно до следующего распределения добычи альянсов.</b>')
            await delete_message_with_notification(mes, m, 5, 5)
            return

        telethon_queue = await db.fetch(r, ['telethon_queue'], one_row=True)
        if not telethon_queue.get('data_bool'):
            m = await mes.answer('<b>[❌] Аккаунт занят своей проверкой. Повторите позже.</b>')
            await delete_message_with_notification(mes, m, 5, 5)
            return

    await db.execute(
        'UPDATE settings SET data_bool = False WHERE var = $1 and var = $2', ['l_check_upd', 'telethon_queue']
    )

    m = await mes.answer('<b>[⚜️] Выполняется проверка локаций, ожидай...</b>')

    r1 = 'SELECT code FROM loc WHERE type != -1 and exist = True'
    r2 = 'SELECT code FROM loc WHERE exist = True'
    req = r1 if mes.get_command().startswith('l_chk') else r2

    result = await client.l_check_method([x.get('code') for x in await db.fetch(req)])

    await client.send_message(config.CW_BOT_ID, '🛡Защита', 1)

    if type(result) is list:
        if result:
            await db.execute(MARK_AS_DEAD_LOCATIONS, [result])
            await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])

            locs = [LocInfoData(**l) for l in await db.fetch(LOC_CHECK_SELECT_DELETED_REQ, [result])]
            t = [
                '<b>{}{}{}</b>\n  └ <code>{}</code>'.format(
                    GET_LOC_TYPE_EMOJI.get(l.type, 'ERROR'), l.name,
                    "" if l.type == LocTypes.ALLIANCE else f" lvl.{l.lvl}", l.code
                ) for l in locs
            ]

            txt = '<b>[🎉] Проверка завершена!</b>\nИстёкшие локации:\n\n' + '\n'.join(t)

        else:
            txt = '<b>[🎉] Проверка завершена!</b>\nИстёкшие локации не обнаружены!'

    else:
        await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])
        await m.edit_text(result)
        return

    # Notifications
    chats = [ChatInfo(**c) for c in await db.fetch(DELETE_LOC_NTF)]

    if chats:
        for chat in chats:
            try:
                await asyncio.sleep(0.3)
                await mes.bot.send_message(chat.id, txt)

            except Exception:
                pass

    await m.edit_text('<b>[🎉] Проверка завершена!</b>')
