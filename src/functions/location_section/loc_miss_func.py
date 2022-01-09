import json

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import LOC_MISS_REQ, LocInfoData, GET_LOC_TYPE_EMOJI, LOC_BUFFS_REQ, LOC_BUFFS_2_REQ, LOC_TYPES_BY_NAME
from src.functions.location_section.loc_info_func import buff_func


async def loc_miss(mes: Message, db: PostgreSQLDatabase):
    res = [LocInfoData(**i) for i in await db.fetch(LOC_MISS_REQ, ['NoneCode%'])]
    if not res:
        await mes.answer('<b><u>🔎Разыскиваемые локации:</u></b>\n\nПусто')
        return

    txt = '\n\n'.join(
        [f'<b>{i}) {GET_LOC_TYPE_EMOJI.get(l.type)}{l.name} lvl.{l.lvl}</b>' for i, l in enumerate(res, start=1)]
    )
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
