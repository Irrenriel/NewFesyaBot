from datetime import datetime, timedelta
from typing import Union

from aiogram.types import Message, CallbackQuery

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import UserData, AL_GET_ALLIANCE_BY_GUILD_REQ, GET_GUILDS_INFO_FOR_PERC
from src.content.texts.alliance_txt import NO_AL_WELCOME, ALLIANCE_MAIN_PAGE_LEADER, ALLIANCE_MAIN_PAGE


async def alliance_main_menu(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.lvl < 15:
        await mes.answer('Извини, но ты пока маловат уровнем и без гильдии.\nТебе тут делать пока нечего!😊')
        return

    if user.guild_tag == 'None':
        await mes.answer('Для участвия в альянсах тебе как минимум нужна гильдия.\nОбнови /hero если уже состоишь.')
        return

    alliance = await db.fetch(AL_GET_ALLIANCE_BY_GUILD_REQ, [user.guild_tag], one_row=True)

    if not alliance:
        kb = InlineKeyboard(Call('❇️Зарегистрировать', 'al:new'), Call('❌Закрыть', 'cancel'))
        await mes.answer(NO_AL_WELCOME, reply_markup=kb)
        return

    await alliance_main_menu_text(mes, db, user)


async def alliance_main_menu_text(mes: Union[Message, CallbackQuery], db: PostgreSQLDatabase, user: UserData):
    alliance = await db.fetch(AL_GET_ALLIANCE_BY_GUILD_REQ, [user.guild_tag], one_row=True)
    func = mes.answer if isinstance(mes, Message) else mes.message.edit_text

    if not alliance:
        kb = InlineKeyboard(Call('❇️Зарегистрировать', 'al:new'), Call('❌Закрыть', 'cancel'))
        await func(NO_AL_WELCOME, reply_markup=kb)
        return

    data = {
        'al_name': alliance['al_name'],
        'al_code': alliance['al_code'],
        'al_owner': alliance['al_owner'],
        'al_leader_username': alliance['al_leader_username'],
        'n_members': str(alliance['n_members']),
        'n_guilds': str(alliance['n_guilds']),
        'al_guilds': ', '.join(alliance['al_guilds'])
    }

    if mes.from_user.id == alliance['al_leader']:
        g_perc, guilds_perc = await get_g_perc(alliance['al_guilds'], db, is_str=True)
        al_perc, main_status, rost_status = await get_al_perc(
            alliance['al_main_last_update'], alliance['al_rost_last_update'], is_str=True
        )

        data.update({
            'al_main_last_update': alliance['al_main_last_update'].strftime('%Y-%m-%d'),
            'al_rost_last_update': alliance['al_rost_last_update'].strftime('%Y-%m-%d'),
            'al_perc': al_perc,
            'main_status': main_status,
            'rost_status': rost_status,
            'g_perc': g_perc,
            'guilds_perc': '\n'.join(guilds_perc)
        })

        await func(ALLIANCE_MAIN_PAGE_LEADER.format(**data))
        return

    await func(ALLIANCE_MAIN_PAGE.format(**data))


async def get_al_perc(main_upd: datetime, roster_upd: datetime, is_str: bool = False):
    diff = datetime.now() - timedelta(days=7)
    perc = 0

    main_status, rost_status = 'Устарел', 'Устарел'

    if main_upd > diff:
        perc += 50
        main_status = 'Актуален'

    if roster_upd > diff:
        perc += 50
        rost_status = 'Актуален'

    return (str(perc) if is_str else perc), main_status, rost_status


async def get_g_perc(guild_tags: list, db: PostgreSQLDatabase, is_str: bool = False):
    guilds_info = await db.fetch(GET_GUILDS_INFO_FOR_PERC, [guild_tags])

    diff = datetime.now() - timedelta(days=7)

    results = []
    progress = guild_tags.copy()

    max_points = len(guild_tags) * 4
    gen_points = 0

    for guild in guilds_info:
        progress.remove(guild['guild_tag'])
        points = 0

        points += 1 if (guild['g_main_raw'] and guild['main_last_upd'] > diff) else 0
        points += 1 if (guild['g_roster_raw'] and guild['roster_last_upd'] > diff) else 0
        points += 1 if (guild['g_atklist_raw'] and guild['atklist_last_upd'] > diff) else 0
        points += 1 if (guild['g_deflist_raw'] and guild['deflist_last_upd'] > diff) else 0

        gen_points += points
        results.append(f'        🏠{guild["guild_tag"]}: {int((points / 4) * 100)}%')

    if progress:
        [results.append(f'        🏠{guild["guild_tag"]}: 0%') for guild in progress]

    x = int((gen_points / max_points) * 100)

    return (str(x) if is_str else x), results
