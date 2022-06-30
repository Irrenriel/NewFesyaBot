import json

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import LOC_MISS_REQ, LocInfoData, GET_LOC_TYPE_EMOJI, LOC_BUFFS_REQ, LOC_BUFFS_2_REQ, LOC_TYPES_BY_NAME
from src.functions.location_section.loc_info_func import buff_func


async def loc_miss(mes: Message, db: PostgreSQLDatabase):
    res = [LocInfoData(**i) for i in await db.fetch(LOC_MISS_REQ, ['NoneCode%'])]
    if not res:
        txt = 'Пусто\n\n'

    else:
        txt = '\n\n'.join(
            [f'<b>{i}) {GET_LOC_TYPE_EMOJI.get(l.type)}{l.name} lvl.{l.lvl}</b>' for i, l in enumerate(res, start=1)]
        )

    count_20 = await db.fetch('SELECT count(*) FROM loc WHERE exist = True and lvl >= 20 and lvl < 40', one_row=True)
    count_40 = await db.fetch('SELECT count(*) FROM loc WHERE exist = True and lvl >= 40 and lvl < 60', one_row=True)
    count_60 = await db.fetch('SELECT count(*) FROM loc WHERE exist = True and lvl >= 60 and lvl < 99', one_row=True)

    l_20 = 6 - count_20.get('count')
    l_40 = 6 - count_40.get('count')
    l_60 = 6 - count_60.get('count')

    if not l_20 and not l_40 and not l_60:
        txt += ''
    else:
        txt += '<b>[❗️] Похоже, есть ещё совсем не обнаруженные локации на этих уровнях:</b>\n'
        if l_20:
            txt += f'   🏅20-39: {l_20} локаций\n'

        if l_40:
            txt += f'   🏅40-59: {l_40} локаций\n'

        if l_60:
            txt += f'   🏅60+: {l_60} локаций\n'

    await mes.answer(f'<b><u>🔎Разыскиваемые локации:</u></b>\n\n{txt}')


async def loc_buffs(mes: Message, db: PostgreSQLDatabase):
    locs = [LocInfoData(**i) for i in await db.fetch(LOC_BUFFS_REQ)]
    buff_locs = await db.fetch(LOC_BUFFS_2_REQ, [[l.code for l in locs]])

    answer = '<b>✨Доступные баффы:</b>\n\n'
    if not buff_locs:
        await mes.answer(answer + 'Нет данных')
        return

    x = []
    for loc in buff_locs:
        _json = json.loads(loc.get('bless_json'))
        info = _json.get('info')

        code, name, lvl = info.get('code'), info.get("name"), info.get("lvl")

        m = f'<a href="https://t.me/share/url?url=/ga_use_{code}">/ga_use_{code}</a>'
        y = f'<b>{LOC_TYPES_BY_NAME.get(name.split(" ")[-1], "error")}{name} lvl.{lvl}</b> ({m})\n'
        x.append(y + await buff_func(_json))

    await mes.answer(answer + '\n\n'.join(x))
