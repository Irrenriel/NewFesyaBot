from aiogram.types import Message

from config import CW_BOT_ID
from resources.models import client
from resources.tools.database import PostgreSQLDatabase
from src.content import UserData, Roles, LOC_CHECK_SELECT_DELETED_REQ, LocInfoData, GET_LOC_TYPE_EMOJI, LocTypes
from src.functions.admin_section.settings_func import delete_message_with_notification


async def loc_check(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.role != Roles.ADMIN:
        l_check_upd = await db.fetch('SELECT data_bool FROM settings WHERE var = $1', ['l_check_upd'], one_row=True)

        if not l_check_upd.get('data_bool'):
            m = await mes.answer('<b>[❌] Не доступно до следующего распределения добычи альянсов.</b>')
            await delete_message_with_notification(mes, m, 5, 5)
            return

    await db.execute('UPDATE settings SET data_bool = False WHERE var = $1', ['l_check_upd'])

    m = await mes.answer('<b>[⚜️] Выполняется проверка локаций, ожидай...</b>')

    r1 = 'SELECT code FROM loc WHERE type != -1 and exist = True'
    r2 = 'SELECT code FROM loc WHERE exist = True'
    req = r1 if mes.get_command().startswith('l_chk') else r2

    result = await client.l_check_method([x.get('code') for x in await db.fetch(req)])

    if type(result) is list:
        if result:
            # await db.execute(
            #     'UPDATE loc SET exist = False, death_time = LOCALTIMESTAMP WHERE code = ANY($1::text[])',
            #     [result]
            # )
            locs = [LocInfoData(**l) for l in await db.fetch(LOC_CHECK_SELECT_DELETED_REQ, [result])]
            t = [
                '<b>{}{}{}</b>\n  └ <code>{}</code>'.format(
                    GET_LOC_TYPE_EMOJI.get(l.type, 'ERROR'), l.name,
                    "" if l.type == LocTypes.ALLIANCE else f" lvl.{l.lvl}", l.code
                ) for l in locs
            ]

            txt = '<b>[🎉] Проверка завершена!</b>\nИстёкшие локации:\n\n' + '\n'.join(t)

        else:
            txt = 'Проверка завершена!\nИстёкшие локации не обнаружены!'

    else:
        await m.edit_text(result)
        return

    # chats = [x[0] for x in mes.db.checkall('SELECT id FROM chats WHERE delete_loc_ntf = 1')]
    # if not chats:
    #     await m.edit_text('Проверка выполнена!')
    #     return
    #
    # for chat in chats:
    #     try:
    #         await bot.send_message(chat, txt)
    #         await asyncio.sleep(0.3)
    #     except:
    #         pass

    await client.send_message(CW_BOT_ID, '🛡Защита', 1)
    await m.edit_text('<b>[🎉] Проверка завершена!</b>')
