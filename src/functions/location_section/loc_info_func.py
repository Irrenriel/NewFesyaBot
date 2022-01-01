import json

from aiogram.types import Message
from asyncpg import Record
from pydantic import BaseModel

from resources.tools.database import PostgreSQLDatabase
from src.content import LocTypes, LOC_TYPES_BY_NUM, AL_INFO_TEXT, LOC_INFO_TEXT


async def loc_info(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_info [код/название локации]')
        return

    loc = await db.fetch(
        'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE code = $1 and exist = True',
        [code], one_row=True
    )

    if not loc:
        loc = await db.fetch(
            'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE name LIKE $1 and exist = True',
            [code + '%'], one_row=True
        )

    answer = await loc_info_answer(mes, db, loc) if loc else 'Данной локации нет в базе данных.'
    await mes.answer(answer, disable_web_page_preview=True)


async def loc_info_answer(mes: Message, db: PostgreSQLDatabase, loc: Record):
    data = LocInfoData(**loc)

    # If Alliance
    if data.type == LocTypes.ALLIANCE:
        # Basic info
        guilds = await db.fetch('SELECT * FROM loc_guilds WHERE code = $1', [data.code])
        roster = ', '.join([f'{l[1]}[{l[2]}]' for l in guilds]) if guilds else 'Нет данных'

        captured_locs = await db.fetch(
            'SELECT code, name, lvl, type FROM loc WHERE conqueror = $1 and exist = True ORDER BY lvl',
            [data.code]
        )

        # Captured locations info
        m = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>{}{} lvl.{}</b></a>'
        cl_txt = '\n'.join(
            [
                m.format(
                    l.get('code'), LOC_TYPES_BY_NUM.get(l.get('type'), 'ERROR'), l.get('name'), str(l.get('lvl'))
                ) for l in captured_locs[:5]
            ]
        ) + '\n...' if len(captured_locs) > 5 else ''

        # History of activity locations
        loc_history = await db.fetch(
            'SELECT data, url, txt FROM loc_history WHERE code = $1 ORDER BY -url LIMIT 5', [data.code]
        )
        mm = '<a href="https://t.me/ChatWarsDigest/{}">{}</a>'
        lh_txt = '\n\n'.join(
            [f'[{mm.format(l.get("url"), l.get("data"))}]\n{l.get("txt")}' for l in loc_history]
        ) if loc_history else 'Нет данных'

        answer = AL_INFO_TEXT.format(
            data.name, data.code, roster, data.code, str(len(captured_locs)), cl_txt, data.code, lh_txt
        )

    # If Other
    else:
        # Basic info
        conq_info = await db.fetch('SELECT name FROM loc WHERE code = $1', [data.conqueror], one_row=True)
        m = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>🎪{}</b></a>'
        conq_txt = m.format(data.conqueror, conq_info.get('name')) if conq_info else 'Нет данных'

        # Resources info if Mine
        res_txt = await res_func(db, data) if data.type == '📦' else ''

        # Buffs info
        buffs = await db.fetch('SELECT bless_json FROM loc_buff where code = $1', [data.code], one_row=True)
        buff_txt = await buff_func(json.loads(buffs.get('bless_json'))) if buffs else 'Нет данных'

        answer = LOC_INFO_TEXT.format(data.type, data.name, str(data.lvl), data.code, conq_txt, res_txt, buff_txt)

    return answer


async def res_func(db: PostgreSQLDatabase, data):
    res_txt = '<b>⛏Ископаемые:</b>\n'

    res = await db.fetch('SELECT res_json FROM loc_res WHERE code = $1', [data.code], one_row=True)
    res_txt += '\n'.join(
        [f'  💎<i>{r}</i>' for r in json.loads(res[0]).get('resources')]
    ) if res else 'Нет данных'
    res_txt += '\n\n'

    return res_txt


async def buff_func(buffs: dict):
    txt = ''
    blesses = buffs.get('blesses')
    for bless in blesses:
        txt += f'    <b>{bless}</b>\n'

        x = blesses.get(bless)
        for i, b in enumerate(x, start=1):
            txt += '    ├ <i>{}({}🎖)</i>\n'.format(*b) if i < len(x) else '    └ <i>{}({}🎖)</i>\n'.format(*b)
    return txt


class LocInfoData(BaseModel):
    code: str
    name: str
    lvl: int
    type: LocTypes
    conqueror: str
    cycle: int
    status: str