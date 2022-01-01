import json
import re
from datetime import datetime, timedelta

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import NEW_LOC_INPUT_PARSE, LOC_TYPES, LOC_TYPES_ENUM, LocTypes, NEW_LOCATION_NOTIFICATION, \
    INCREASE_LOCATION_TOP_COUNT_REQ, UserData, INSERT_OR_UPDATE_LOCATION_BUFF_REQ, INSERT_OR_UPDATE_LOCATION_RES_REQ
from src.functions.admin_section.settings_func import delete_message_with_notification


# Reception of locations from CW quests
async def new_location_input(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if not datetime.now() - mes.forward_date < timedelta(days=2):
        return

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
    l_conq = 'headquarter' if l_type == LocTypes.ALLIANCE else None

    check = await db.fetch('SELECT code from loc WHERE name = $1 and lvl = $2', [l_name, l_lvl], one_row=True)
    u = mes.from_user.username if mes.from_user.username else mes.from_user.first_name + '_FirstName'
    if check and check.get('code').startswith('NoneCode'):
        await db.execute('UPDATE loc SET code = $1, f_by = $2, f_by_guild = $3 WHERE name = $4 and lvl = $5',
                         [l_code, u, user.guild_tag if user else 'None', l_name, l_lvl])

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
    # ! ! ! ! !
    # answer = l_type + l_name + ("" if l_lvl == 99 else " lvl. " + str(l_lvl))
    # txt = NEW_LOCATION_NOTIFICATION.format(answer, l_code)
    #
    # chats = mes.db.checkall('SELECT id FROM chats WHERE new_loc_ntf = 1', [])
    #
    # if not chats:
    #     await mes.answer('Новая локация! {}'.format(
    #         'Зачислен +1 балл! (/top)' if top else 'Балл не засчитан, требуется регистрация.'))
    #     return
    #
    # for chat in chats:
    #     try:
    #         await bot.send_message(chat[0], text)
    #     except:
    #         pass
    #     await asyncio.sleep(0.3)
    # ! ! ! ! !

    # Reward
    await db.execute(INCREASE_LOCATION_TOP_COUNT_REQ, [mes.from_user.id])

    if user:
        top = await db.fetch('SELECT count FROM location_top WHERE uid = $1', [mes.from_user.id], one_row=True)
        c = top.get("count") if top else 1
        txt = f'<b>[🎉] Обнаружена новая локация! Вам зачислен балл!</b>\nПодробнее: /top1 (всего баллов — {c})'

    else:
        txt = f'<b>[🎉] Обнаружена новая локация! Вам зачислен балл, но без регистрации ваш счёт не учитывается.</b>'

    await mes.answer(txt)


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
