import asyncio
import datetime
from typing import Union

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified

from resources.tools.database import PostgreSQLDatabase
from src.content import LOC_LIST_TEXT, LOC_OBJECTS_REQ, LocInfoData, GET_LOC_TYPE_EMOJI, LOC_CAPTURE_REQ, \
    LOC_MAP_BY_TIER_REQ, LOC_MAP_BY_TYPE_REQ


async def loc_list(mes: Union[Message, CallbackQuery], db: PostgreSQLDatabase):
    alliance_len = await db.fetch('SELECT count(*) FROM loc WHERE type = -1 and exist = True', one_row=True)
    ruins_len = await db.fetch('SELECT count(*) FROM loc WHERE type = 1 and exist = True', one_row=True)
    mines_len = await db.fetch('SELECT count(*) FROM loc WHERE type = 2 and exist = True', one_row=True)
    forts_len = await db.fetch('SELECT count(*) FROM loc WHERE type = 3 and exist = True', one_row=True)

    last_update = await db.fetch('SELECT date FROM settings_date WHERE var = $1', ['l_check_upd'], one_row=True)

    txt = LOC_LIST_TEXT.format(
        str(ruins_len.get('count')), str(mines_len.get('count')), str(forts_len.get('count')),
        str(alliance_len.get('count')), '❌',
        last_update.get('date').strftime('%H:%M:%S %d-%m-%Y') if last_update else ''
    )

    try:
        if isinstance(mes, Message):
            await mes.answer(txt, reply_markup=loc_list_kb())

        else:
            await mes.message.edit_text(txt, reply_markup=loc_list_kb())
            await mes.answer()

    except MessageNotModified:
        await mes.answer()


async def loc_list_objects(call: CallbackQuery, db: PostgreSQLDatabase):
    callback_datas = {
        'll:al': {'text': '[🎪] Альянсы', 'type': -1}, 'll:ruins': {'text': '[🏷] Руины', 'type': 1},
        'll:mines': {'text': '[📦] Шахты', 'type': 2}, 'll:forts': {'text': '[🎖] Форты', 'type': 3},
    }

    data = callback_datas.get(call.data)
    if not data:
        return

    txt = f'<b>{data["text"]}</b>\n\n'

    result = [LocInfoData(**i) for i in await db.fetch(LOC_OBJECTS_REQ, [data['type']])]
    if result:
        txt += '\n\n'.join(
            f'<b>{i}) {GET_LOC_TYPE_EMOJI.get(l.type)}{l.name} lvl. {l.lvl}</b> — <code>{l.code}</code>'
            for i, l in enumerate(result, start=1)
        )

    else:
        txt += 'Нет данных'

    try:
        await call.message.edit_text(txt, reply_markup=loc_list_kb())
        await call.answer()

    except MessageNotModified:
        await call.answer()


async def loc_list_map(call: CallbackQuery, db: PostgreSQLDatabase):
    callback_datas = {
        'default': {'text': '[🚩] Карта', 'type': 0},
        'by_tier': {'text': '[🏅] Карта', 'type': 1},
        'by_type': {'text': '[💠] Карта', 'type': 2}
    }

    data = callback_datas.get(call.data.split(':')[-1])
    if not data:
        return

    txt = f'<b>{data["text"]}</b>\n\n'

    alliances = [LocInfoData(**i) for i in await db.fetch(LOC_OBJECTS_REQ, [-1])]
    if not alliances:
        try:
            await call.message.edit_text(txt + 'Нет данных', reply_markup=loc_list_kb())

        except MessageNotModified:
            await call.answer()

        finally:
            return

    if data['type'] == 0:
        txt = await loc_list_map_default(alliances, db, txt)

    elif data['type'] == 1:
        txt = await loc_list_map_by_tiers(alliances, db, txt)

    elif data['type'] == 2:
        txt = await loc_list_map_by_types(alliances, db, txt)

    else:
        await call.answer()
        return

    try:
        await call.message.edit_text(txt, reply_markup=loc_list_kb())
        await call.answer()

    except MessageNotModified:
        await call.answer()


async def loc_list_map_default(alliances: list, db: PostgreSQLDatabase, txt: str):
    m = '<a href="https://t.me/share/url?url=/l_info%20{}">{}</a>'
    for al in alliances:
        # All locations of alliance
        locs = [LocInfoData(**i) for i in await db.fetch(LOC_CAPTURE_REQ, [al.code])]
        if not locs:
            continue

        # String with alliance
        txt += f'<b>⚜🎪{m.format(al.code, al.name)} ({len(locs)}):</b>\n'

        # Strings with locations
        for l in locs:
            x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
            txt += f'   {m.format(l.code, x)} [{l.cycle}{l.status}]\n'
        txt += '\n'

    empty_locs = [LocInfoData(**i) for i in await db.fetch(LOC_CAPTURE_REQ, ["Forbidden Clan"])]
    len_el = len(empty_locs)

    # String with Forbidden Clan
    txt += f'<b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'

    # Strings with locations
    if not len_el:
        return txt

    for l in empty_locs:
        x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
        txt += f'   {m.format(l.code, x)}\n'
    return txt


async def loc_list_map_by_tiers(alliances: list, db: PostgreSQLDatabase, txt: str):
    d = {
        '0': {'text': '20-39', 'f': 20, 't': 39},
        '1': {'text': '40-59', 'f': 40, 't': 59},
        '2': {'text': '60+', 'f': 60, 't': 98},
    }

    result = await asyncio.gather(
        *[loc_list_map_by_tier(alliances, db, d[str(i)]) for i in range(3)]
    )

    return txt + '\n\n'.join(result)


async def loc_list_map_by_types(alliances: list, db: PostgreSQLDatabase, txt: str):
    d = {
        '0': {'text': '🏷Руины', 'type': 1},
        '1': {'text': '📦Шахты', 'type': 2},
        '2': {'text': '🎖Форты', 'type': 3},
    }

    result = await asyncio.gather(
        *[loc_list_map_by_type(alliances, db, d[str(i)]) for i in range(3)]
    )

    return txt + '\n\n'.join(result)


async def loc_list_map_by_tier(alliances: list, db: PostgreSQLDatabase, kwargs: dict):
    m = '<a href="https://t.me/share/url?url=/l_info%20{}">{}</a>'
    txt = f'<b>🏅{kwargs["text"]}:</b>\n'

    for al in alliances:
        # All locations of alliance
        locs = [
            LocInfoData(**i) for i in await db.fetch(LOC_MAP_BY_TIER_REQ, [al.code, kwargs['f'], kwargs['t']])
        ]
        if not locs:
            continue

        # String with alliance
        txt += f'   <b>⚜🎪{m.format(al.code, al.name)} ({len(locs)}):</b>\n'

        # Strings with locations
        for l in locs:
            x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
            txt += f'      {m.format(l.code, x)} [{l.cycle}{l.status}]\n'
        txt += '\n'

    empty_locs = [
        LocInfoData(**i) for i in await db.fetch(LOC_MAP_BY_TIER_REQ, ["Forbidden Clan", kwargs['f'], kwargs['t']])
    ]
    len_el = len(empty_locs)

    # String with Forbidden Clan
    txt += f'   <b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'

    # Strings with locations
    if not len_el:
        return txt

    for l in empty_locs:
        x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
        txt += f'       {m.format(l.code, x)}\n'
    return txt


async def loc_list_map_by_type(alliances: list, db: PostgreSQLDatabase, kwargs: dict):
    m = '<a href="https://t.me/share/url?url=/l_info%20{}">{}</a>'
    txt = f'<b>{kwargs["text"]}:</b>\n'

    for al in alliances:
        # All locations of alliance
        locs = [
            LocInfoData(**i) for i in await db.fetch(LOC_MAP_BY_TYPE_REQ, [al.code, kwargs['type']])
        ]
        if not locs:
            continue

        # String with alliance
        txt += f'   <b>⚜🎪{m.format(al.code, al.name)} ({len(locs)}):</b>\n'

        # Strings with locations
        for l in locs:
            x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
            txt += f'      {m.format(l.code, x)} [{l.cycle}{l.status}]\n'
        txt += '\n'

    empty_locs = [
        LocInfoData(**i) for i in await db.fetch(LOC_MAP_BY_TYPE_REQ, ["Forbidden Clan", kwargs['type']])
    ]
    len_el = len(empty_locs)

    # String with Forbidden Clan
    txt += f'   <b>🏴‍☠ Forbidden Clan ({len_el})</b>{":" if len_el else ""}\n'

    # Strings with locations
    if not len_el:
        return txt

    for l in empty_locs:
        x = f'{GET_LOC_TYPE_EMOJI.get(l.type)}{name_format(l.name)} lvl.{l.lvl}'
        txt += f'       {m.format(l.code, x)}\n'
    return txt


def name_format(name: str, i: int = 2):
    words = name.split(' ')
    if len(words) == 1:
        return name

    while True:
        if words[0][i] in 'aeiou':
            i += 1
        else:
            return f'{words[0][:i+1]}. {words[1]}'


def loc_list_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='🏷', callback_data='ll:ruins'),
            InlineKeyboardButton(text='📦', callback_data='ll:mines'),
            InlineKeyboardButton(text='🎖', callback_data='ll:forts'),
            InlineKeyboardButton(text='🎪', callback_data='ll:al')
        ],
        [
            InlineKeyboardButton(text='🚩', callback_data='ll:map:default'),
            InlineKeyboardButton(text='🏅', callback_data='ll:map:by_tier'),
            InlineKeyboardButton(text='💠', callback_data='ll:map:by_type')
        ],
        [
            InlineKeyboardButton(text='Меню', callback_data='ll:menu'),
            InlineKeyboardButton(text='Закрыть', callback_data='ll:cancel')
        ]
    ])
