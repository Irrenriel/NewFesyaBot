import json

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import LocTypes, AL_INFO_TEXT, LOC_INFO_TEXT, LOC_HISTORY_REQ, AL_HISTORY_TEXT, LOC_CAPTURE_REQ, \
    AL_CAPTURE_TEXT, LocInfoData, LocHistoryData, GET_LOC_TYPE_EMOJI, LOC_INFO_REQ, LOC_INFO_2_REQ, \
    LOC_INFO_GUILD_INFO, LocGuildInfo


async def loc_info(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_info [код/название локации]')
        return

    loc = await db.fetch(LOC_INFO_REQ, [code], one_row=True)
    if not loc:
        loc = await db.fetch(LOC_INFO_2_REQ, [code + '%'], one_row=True)

    answer = await loc_info_answer(db, LocInfoData(**loc)) if loc else 'Данной локации нет в базе данных.'
    await mes.answer(answer, disable_web_page_preview=True)


async def loc_info_answer(db: PostgreSQLDatabase, loc: LocInfoData):
    # If Alliance
    if loc.type == LocTypes.ALLIANCE:
        # Basic info
        guilds = [LocGuildInfo(**i) for i in await db.fetch(LOC_INFO_GUILD_INFO, [loc.code])]
        roster = ', '.join([f'{l.guild_emoji}[{l.guild_tag}]' for l in guilds]) if guilds else 'Нет данных'

        captured_locs = [LocInfoData(**i) for i in await db.fetch(LOC_CAPTURE_REQ, [loc.code])]

        # Captured locations info
        m = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>{}{} lvl.{}</b></a>'
        cl_txt = '\n'.join(
            [m.format(l.code, GET_LOC_TYPE_EMOJI.get(l.type, 'ERROR'), l.name, str(l.lvl)) for l in captured_locs[:5]]
        ) + ('\n...' if len(captured_locs) > 5 else '')

        # History of activity locations
        l_history = [LocHistoryData(**i) for i in await db.fetch(LOC_HISTORY_REQ, [loc.code, 5])]
        mm = '<a href="https://t.me/ChatWarsDigest/{}">{}</a>'
        lh_txt = '\n\n'.join(
            [f'[{mm.format(l.url, l.date)}]\n{l.txt}' for l in l_history]
        ) if l_history else 'Нет данных'

        answer = AL_INFO_TEXT.format(
            loc.name, loc.code, roster, loc.code, str(len(captured_locs)), cl_txt, loc.code, lh_txt
        )

    # If Other
    else:
        # Basic info
        conq_info = await db.fetch('SELECT name FROM loc WHERE code = $1', [loc.conqueror], one_row=True)

        m = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>🎪{}</b></a>'
        conq_txt = m.format(loc.conqueror, conq_info.get('name')) if conq_info else 'Нет данных'

        # Resources info if Mine
        res_txt = await res_func(db, loc) if loc.type == LocTypes.MINE else ''

        # Buffs info
        buffs = await db.fetch('SELECT bless_json FROM loc_buff where code = $1', [loc.code], one_row=True)
        buff_txt = await buff_func(json.loads(buffs.get('bless_json'))) if buffs else 'Нет данных'

        answer = LOC_INFO_TEXT.format(
            GET_LOC_TYPE_EMOJI.get(loc.type), loc.name, str(loc.lvl), loc.code, conq_txt, res_txt, buff_txt
        )

    return answer


async def res_func(db: PostgreSQLDatabase, loc: LocInfoData):
    res_txt = '<b>⛏Ископаемые:</b>\n'

    res = await db.fetch('SELECT res_json FROM loc_res WHERE code = $1', [loc.code], one_row=True)
    res_txt += '\n'.join(
        [f'  💎<i>{r}</i>' for r in json.loads(res.get('res_json')).get('resources')]
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


async def loc_history(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_history [код]')
        return

    loc = await db.fetch('SELECT type FROM loc WHERE code = $1 and exist = True', [code], one_row=True)
    if not loc:
        await mes.answer('Данной локации нет в базе данных.')
        return

    if loc.get('type') != -1:
        await mes.answer('Информация доступна только по альянсам.')
        return

    l_history = [LocHistoryData(**i) for i in await db.fetch(LOC_HISTORY_REQ, [code, 20])]

    m = '<a href="https://t.me/ChatWarsDigest/{}">{}</a>'
    lh_txt = '\n\n'.join(
        f'[{m.format(str(l.url), str(l.date))}]\n{l.txt}' for l in l_history
    ) if l_history else 'Нет данных'

    await mes.answer(AL_HISTORY_TEXT.format(code, lh_txt), disable_web_page_preview=True)


async def loc_capture(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_capture [код]')
        return

    loc = await db.fetch('SELECT type FROM loc WHERE code = $1 and exist = True', [code], one_row=True)
    if not loc:
        await mes.answer('Данной локации нет в базе данных.')
        return

    if loc.get('type') != -1:
        await mes.answer('Информация доступна только по альянсам.')
        return

    captured_locs = [LocInfoData(**i) for i in await db.fetch(LOC_CAPTURE_REQ, [code])]

    m = '<a href="https://t.me/share/url?url=/l_info%20{}"><b>{}{} lvl.{}</b></a>'
    cl_txt = '\n'.join(
        m.format(l.code, GET_LOC_TYPE_EMOJI.get(l.type), l.name, str(l.lvl)) for l in captured_locs
    ) if captured_locs else 'Нет данных'

    await mes.answer(AL_CAPTURE_TEXT.format(code, cl_txt), disable_web_page_preview=True)
