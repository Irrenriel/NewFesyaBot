import asyncio
import json
import re
from datetime import datetime, timedelta
from logging import warning

from aiogram.types import Message
from asyncpg import Record

from config import config
from resources.models import client
from resources.tools.database import PostgreSQLDatabase
from src.content import NEW_LOC_INPUT_PARSE, LOC_TYPES_ENUM, LocTypes, NEW_LOCATION_NOTIFICATION, \
    INCREASE_LOCATION_TOP_COUNT_REQ, UserData, INSERT_OR_UPDATE_LOCATION_BUFF_REQ, INSERT_OR_UPDATE_LOCATION_RES_REQ, \
    LocInfoData, NEW_LOC_L_CHECK_FOR_TIER, GET_LOC_TYPE_EMOJI, LOC_CHECK_SELECT_DELETED_REQ, MARK_AS_DEAD_LOCATIONS, \
    NEW_LOC_NTF, NEW_LOCATION_TEXT, DELETE_LOC_NTF
from src.content.consts.main_resources import ChatInfo
from src.functions.admin_section.settings_func import delete_message_with_notification


# Reception of locations from CW quests
async def new_location_input(mes: Message, db: PostgreSQLDatabase, user: UserData):
    # if not datetime.now() - mes.forward_date < timedelta(days=2):
    #     return

    # Definition is location or alliance and packing into dictionary
    result = re.search(NEW_LOC_INPUT_PARSE, mes.text).groupdict()
    result = {k: v for k, v in result.items() if v is not None}
    l_code = result.get("loc_code", result.get("head_code"))

    # Determining whether a given location is in the database
    if await db.fetch('SELECT * FROM loc WHERE code = $1', [l_code], one_row=True):
        m = await mes.answer('<b>[❌] Данная локация уже есть в базе.</b>')
        await delete_message_with_notification(mes, m, 5, 5)
        return

    l_name = result.get("loc_name", result.get("head_name"))
    l_lvl = int(result.get("loc_lvl", "99"))

    l_type = LOC_TYPES_ENUM.get(l_name.split(' ')[-1], LocTypes.ALLIANCE)
    if l_type == LocTypes.FORT and ' ' in l_name:
        l_type = LocTypes.ALLIANCE

    l_conq = 'headquarter' if l_type == LocTypes.ALLIANCE else None

    check = await db.fetch('SELECT code from loc WHERE name = $1 and lvl = $2', [l_name, l_lvl], one_row=True)
    u = mes.from_user.username if mes.from_user.username else mes.from_user.first_name + '_FirstName'

    if check and check.get('code').startswith('NoneCode'):
        await db.execute(
            'UPDATE loc SET code = $1, f_by = $2, f_by_guild = $3 WHERE name = $4 and lvl = $5',
            [l_code, u, user.guild_tag if user else 'None', l_name, l_lvl]
        )

    elif l_conq:
        await db.execute(
            'INSERT INTO loc (code, name, lvl, type, conqueror, f_by, f_by_guild) VALUES ($1, $2, $3, $4, $5, $6, $7)',
            [l_code, l_name, l_lvl, l_type.value, l_conq, u, user.guild_tag if user else 'None']
        )

    else:
        await db.execute(
            'INSERT INTO loc (code, name, lvl, type, f_by, f_by_guild) VALUES ($1, $2, $3, $4, $5, $6)',
            [l_code, l_name, l_lvl, l_type.value, u, user.guild_tag if user else 'None']
        )

    # Notifications
    chats = [ChatInfo(**c) for c in await db.fetch(NEW_LOC_NTF)]

    if chats:
        answer = NEW_LOCATION_TEXT.format(
            type=GET_LOC_TYPE_EMOJI.get(l_type, 'Error'), name=l_name, lvl='' if l_lvl == 99 else f' lvl.{l_lvl}',
            code=l_code
        )

        for chat in chats:
            try:
                await asyncio.sleep(0.3)
                await mes.bot.send_message(chat.id, answer)

            except Exception:
                pass

    # Reward
    await db.execute(INCREASE_LOCATION_TOP_COUNT_REQ, [mes.from_user.id])

    if user:
        top = await db.fetch('SELECT count FROM location_top WHERE uid = $1', [mes.from_user.id], one_row=True)
        c = top.get("count") if top else 1
        txt = f'<b>[🎉] Обнаружена новая локация! Вам зачислен балл!</b>\nПодробнее: /top1 (всего баллов — {c})'

    else:
        txt = f'<b>[🎉] Обнаружена новая локация! Вам зачислен балл, но без регистрации ваш счёт не учитывается.</b>'

    await mes.answer(txt)

    # Tier
    if l_type == LocTypes.ALLIANCE:
        return

    # Settings Check
    x = await db.fetch('SELECT data_bool FROM settings WHERE var = $1', ['telethon_queue'], one_row=True)
    if not isinstance(x, Record) or not x.get('data_bool'):
        try:
            await mes.bot.send_message(
                (await client.client.get_me()).id,
                '[❗️] Найдено больше 6 локаций одного тира, но не удаётся проверить. Идёт другая проверка'
            )

        except Exception as e:
            warning(f'Exception Happend: {type(e)} - {e}')

        return

    if 20 <= l_lvl < 40:
        f, t = 20, 40

    elif 40 <= l_lvl < 60:
        f, t = 40, 60

    else:
        f, t = 40, 99

    locs_of_tier = await db.fetch(NEW_LOC_L_CHECK_FOR_TIER, [f, t])
    if not locs_of_tier or len(locs_of_tier) < 7:
        return

    # Disable l_check
    await db.execute('UPDATE settings SET data_bool = False WHERE var = $1', ['l_check_upd'])
    result = await client.l_check_method([x.get('code') for x in locs_of_tier])
    await client.send_message(config.CW_BOT_ID, '🛡Защита', 1)

    if type(result) is list:
        if not result:
            try:
                await mes.bot.send_message(
                    (await client.client.get_me()).id,
                    '[❗️] Найдено больше 6 локаций одного тира, но не удаётся проверить. Аккаунт чем-то занят.'
                )

            except Exception as e:
                warning(f'Exception Happend: {type(e)} - {e}')
            return

        await db.execute(MARK_AS_DEAD_LOCATIONS, [result])
        await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])

        locs = [LocInfoData(**l) for l in await db.fetch(LOC_CHECK_SELECT_DELETED_REQ, [result])]
        t = [
            '<b>{}{}{}</b>\n  └ <code>{}</code>'.format(
                GET_LOC_TYPE_EMOJI.get(l.type, 'ERROR'), l.name,
                "" if l.type == LocTypes.ALLIANCE else f" lvl.{l.lvl}", l.code
            ) for l in locs
        ]

        # Notifications
        chats = [ChatInfo(**c) for c in await db.fetch(DELETE_LOC_NTF)]

        if chats:
            answer = '<b>[🎉] Проверка завершена!</b>\nИстёкшие локации:\n\n' + "\n".join(t)

            for chat in chats:
                try:
                    await asyncio.sleep(0.3)
                    await mes.bot.send_message(chat.id, answer)

                except Exception:
                    pass


# Reception of blessing from locations
async def new_bless_input(mes: Message, db: PostgreSQLDatabase):
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        return

    code = re.search(r'ga_use_(.+)_', mes.text).group(1)
    if not await db.fetch('SELECT * FROm loc WHERE code = $1 and exist = True', [code], one_row=True):
        await mes.answer('[❌] Данной локации нет в базе данных.')

    container = mes.text.split(' attractions:\n')

    loc_info = re.search(r'(?P<name>\w.+) lvl\.(?P<lvl>\d+)', container[0])
    info = {'code': code, 'name': loc_info.group('name'), 'lvl': int(loc_info.group('lvl'))}

    blesses = {}
    for el in container[1].split('✨')[1:]:
        bless_type = el.split('\n')[0]
        temp = []

        for l in el.replace(bless_type + '\n', '').split('🎖\n'):
            if not l:
                continue
            s = l.split('\n')
            temp.append([s[0][2:], int(re.search(r'Price: (\d+)', s[2]).group(1))])

        blesses[bless_type] = temp

    x = await db.fetch('SELECT * FROM loc_buff WHERE code = $1', [code], one_row=True)
    await db.execute(INSERT_OR_UPDATE_LOCATION_BUFF_REQ, [code, json.dumps({'info': info, 'blesses': blesses})])

    if x:
        await mes.answer(f'[✨] Перезаписаны баффы к <code>{code}</code> локации!')
    else:
        await mes.answer(f'[✨] Записаны баффы к <code>{code}</code> локации!')


# Reception of resources from locations
async def new_res_input(mes: Message, db: PostgreSQLDatabase):
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        return

    pool = mes.text.split('\n\n')[1:]
    locs = [x.get('code') for x in await db.fetch('SELECT code FROM loc WHERE exist = True')]

    input = []
    for loc in pool:
        parse = re.search(r'(?P<name>.+) lvl\.\d+\n.+Code: (?P<code>\S+)\.', loc)
        if not parse or ('Mine' not in parse.group('name')):
            continue

        code = parse.group('code')
        if code not in locs:
            continue

        resources = []
        for r in loc.split(f'Code: {code}.\n')[1].split('\n'):
            x = r.split(':')[0]
            if x == 'Attractions':
                continue
            resources.append(x)

        input.append((code, json.dumps({'resources': resources})))

    if input:
        await db.execute(INSERT_OR_UPDATE_LOCATION_RES_REQ, input, many=True)
        await mes.answer(f'[💎] Обновлены ресурсы у {len(input)} шахт!')

    else:
        await mes.answer('[💎] Шахты не найдены!')
