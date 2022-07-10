import asyncio
import logging
import re
import sys
import traceback
from logging import warning
from typing import Optional, List

from aiogram import Bot
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import Message

from config import config
from resources.tools import bot_logging
from resources.tools.database import PostgreSQLDatabase
from src.content import BRIEF_ALLIANCE_PARSE, STATUS_HEADQUARTERS_DICT, BRIEF_GET_ALLIANCE_BY_GUILD_TAG, \
    BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL, HQParsingData, ChatInfo, BRIEF_NTF_REQ, BRIEF_LOCATIONS_PARSE, LocInfoData, \
    BRIEF_GET_ALL_LOCS_REQ, STATUS_LOCATIONS_DICT, LocParsingData, FORBIDDEN_CLASSES, BRIEF_INSERT_GUILD_REQ, \
    BRIEF_GET_LOC_INFO_BY_NAME_REQ


def main():
    loop = asyncio.get_event_loop()
    client = TelegramClient(config.BRIEF_SESSION_NAME, config.API_ID, config.API_HASH, loop=loop)
    bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=config.PARSE_MODE)

    # Database
    db = PostgreSQLDatabase(*config.BRIEF_DB)

    channels = [config.MY_TESTING_CHANNEL, config.CHAT_WARS_DIGEST, 1746905360]

    @client.on(NewMessage(chats=channels, func=lambda c: '🤝Headquarters news:' in c.message.message))
    async def brief_headquarters(event: NewMessage.Event):
        # Вспомогательные функции
        async def hq_parsing(hq: str) -> Optional[HQParsingData]:
            parse = re.search(BRIEF_ALLIANCE_PARSE, hq)

            if not parse:
                warning(f'Can`t parse headquarter event: "{hq}"')
                return

            parse_data = parse.groupdict()

            code_by_name = await db.fetch(
                'SELECT code FROM loc WHERE name = $1', [parse_data['head_name']], one_row=True
            )

            parse_data['code'] = code_by_name['code'] if code_by_name else f'NoneCode({parse_data["head_name"]})'
            parse_data['status'] = STATUS_HEADQUARTERS_DICT.get(parse_data['status'])
            parse_data['stock'] = parse_data.get('stock', '0')
            parse_data['glory'] = parse_data.get('glory', '0')

            return HQParsingData(**parse_data)

        async def hq_attackers_parsing(line: str, hq: str):
            attackers = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
            hq_data.atk_answer = '🎖⚔: {}\n'.format(','.join(['{}[{}]'.format(*i) for i in attackers]))

            if 'breached' not in hq:
                return

            async def temp_raider(tag: str):
                raid_hq = await db.fetch(BRIEF_GET_ALLIANCE_BY_GUILD_TAG, [tag], one_row=True)
                raider_name = raid_hq['name'] if raid_hq else f'NoneQuart({tag})'

                raiders.add(raider_name)

                # Запись кто пробил
                await db.execute(
                    BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL,
                    hq_data.breaching_raider_log(raid_hq['code'] if raid_hq else raider_name)
                )

            raiders = set()
            await asyncio.gather(*[temp_raider(tag) for em, tag in attackers])

            hq_data.breach = f'➖🎁: -{hq_data.stock}📦, -{hq_data.glory}🎖\n'

            # Запись кого пробили
            await db.execute(BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL, hq_data.breached_hq_log(raiders))

        async def hq_defenders_parsing(line: str):
            defenders = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
            hq_data.def_answer = '🎖🛡: {}\n'.format(','.join(['{}[{}]'.format(i[0], i[1]) for i in defenders]))

        # Начало обработки
        message: Message = event.message

        answer_long = answer_short = '<i>🤝Альянсы:</i>\n'

        # Datetime
        raw_date, date, mid = get_date_and_message_id(message)

        for hq in message.message.replace('🤝Headquarters news:\n', '').split('\n\n\n'):
            hq_data = await hq_parsing(hq)

            if not hq_data:
                continue

            # Datetime
            hq_data.hq_date(raw_date, mid)

            # Эту хуйню надо срочно доработать под чаты!
            if hq_data.name == 'Alert Eyes':
                hq_data.own = '🔷'

            for line in hq.splitlines():
                if '🎖Attack:' in line:
                    await hq_attackers_parsing(line, hq)

                elif '🎖Defense:' in line:
                    await hq_defenders_parsing(line)

            answer_long += hq_data.get_answer_mode_long
            answer_short += hq_data.get_answer_mode_short

        ending = get_ending(date, mid)

        answer_long += ending
        answer_short += ending

        # Notifications
        chats: List[ChatInfo] = await db.fetch_orm(ChatInfo, BRIEF_NTF_REQ)
        if not chats:
            return

        for chat in chats:
            try:
                await bot.send_message(chat.id, answer_short if chat.brief_mode else answer_long)

            except Exception:
                logging.error(traceback.format_exc())

    @client.on(NewMessage(chats=channels, func=lambda c: '🗺State of map:' in c.message.message))
    async def brief_locations(event: NewMessage.Event):
        # Вспомогательные функции
        async def loc_parsing(loc: str) -> Optional[LocParsingData]:
            parse = re.search(BRIEF_LOCATIONS_PARSE, loc)

            if not parse:
                warning(f'Can`t parse location event: "{loc}"')
                return

            parse_data = parse.groupdict()

            parse_data['lvl'] = int(parse_data['lvl'])
            parse_data['status'] = STATUS_LOCATIONS_DICT.get(
                parse_data.get('def_status', parse_data.get('atk_status'))
            )
            parse_data['new_conqueror'] = parse_data.get('new_conqueror', '')

            for l in all_locations:
                if l.name == parse_data['name'] and l.lvl == parse_data['lvl']:
                    all_locations.remove(l)
                    break

            # Проверяет что такая локация есть в БД
            code_by_name_and_lvl = await db.fetch(
                'SELECT code, conqueror FROM loc WHERE name = $1 AND lvl = $2 AND exist = True',
                [parse_data['name'], parse_data['lvl']], one_row=True
            )

            if code_by_name_and_lvl:
                parse_data['code'] = code_by_name_and_lvl['code']
                parse_data['prev_conqueror'] = code_by_name_and_lvl['conqueror']

            else:
                parse_data['code'] = f'NoneCode({parse_data["name"]} lvl.{parse_data["lvl"]})'

            return LocParsingData(**parse_data)

        async def loc_attackers_parsing(line: str):
            attackers = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
            loc_data.atk_answer = '🎖⚔: {}\n'.format(','.join(['{}[{}]'.format(i[0], i[1]) for i in attackers]))

        async def loc_defenders_parsing(line: str):
            # Проверка кто на дефе стоит
            if 'Forbidden' in line:
                defenders = set(re.findall(r'Forbidden (?P<mob_class>\w+) lvl(?P<mob_lvl>\d+)', line))
                loc_data.def_answer += '🎖🛡: {}\n'.format(
                    ','.join([f'🏴‍☠[{FORBIDDEN_CLASSES.get(i[0], "error")}]' for i in defenders])
                )

            elif 'Golem' in line:
                defenders = set(re.findall(r'Golem (?P<mob_class>\w+) lvl(?P<mob_lvl>\d+)', line))
                loc_data.def_answer += '🎖🛡: {}\n'.format(
                    ','.join([f'🤖[{FORBIDDEN_CLASSES.get(i[0], "error")}]' for i in defenders])
                )

            else:
                defenders = set(re.findall(r'(?P<castle_guild_emoji>\S+)\[(?P<guild>...?)\]', line))
                loc_data.def_answer += '🎖🛡: {}\n'.format(
                    ','.join([f'{i[0]}[{i[1]}]' for i in defenders])
                )

            if loc_data.prev_conqueror != 'Forbidden Clan' and 'Forbidden' not in line and 'Golem' not in line:
                await db.execute(
                    BRIEF_INSERT_GUILD_REQ, [[loc_data.prev_conqueror, d[1], d[0]] for d in defenders], many=True
                )

        async def loc_conquest():
            new_conqueror: LocInfoData = await db.fetch_orm(
                LocInfoData, BRIEF_GET_LOC_INFO_BY_NAME_REQ, [loc_data.new_conqueror], one_row=True
            )

            loc_data.new_conqueror_code = new_conqueror.code if new_conqueror else f'NoneCode({loc_data.new_conqueror})'

            # Set Work Status "⏳" and New Conqueror
            await db.execute(
                'UPDATE loc SET status = $1, conqueror = $2 WHERE name = $3 AND lvl = $4 AND exist = True',
                ["⏳", loc_data.new_conqueror_code, loc_data.name, loc_data.lvl]
            )

            if new_conqueror:
                await db.execute(BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL, loc_data.loc_conquest_log)

            if loc_data.prev_conqueror != 'Forbidden Clan':
                await db.execute(BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL, loc_data.loc_failed_defend_log)


        # Начало обработки
        message: Message = event.message

        all_locations: List[LocInfoData] = await db.fetch_orm(LocInfoData, BRIEF_GET_ALL_LOCS_REQ)

        lt = {'🏷': [], '📦': [], '🎖': []}

        answer_long = answer_short = '<i>🗺Локации:</i>\n'

        # Datetime
        raw_date, date, mid = get_date_and_message_id(message)

        for loc in message.message.replace('🗺State of map:', '').split('\n\n'):
            '''
            Так в брифинге отображаются новые появившиеся локации, желательно в брифинге сделать и на алики,
            и на локации оповещение о новых локациях!
            '''
            if '🎖Attack:' not in loc and '🎖Defense:' not in loc:
                return

            loc_data = await loc_parsing(loc)

            # Datetime
            loc_data.loc_date(raw_date, mid)

            # Эту хуйню надо срочно доработать под чаты!
            if loc_data.name == 'Alert Eyes':
                loc_data.own = '🔷'

            for line in loc.splitlines():
                if '🎖Attack:' in line:
                    await loc_attackers_parsing(line)

                elif '🎖Defense:' in line:
                    await loc_defenders_parsing(line)

            if 'belongs to' in loc:
                await loc_conquest()

            elif ('Forbidden' not in loc) and ('Golem' not in loc):
                await db.execute('UPDATE loc SET status = $1, cycle = cycle + 1 WHERE code = $2', ["⚡", loc_data.code])

            # Записываем какой это типа локации
            lt[loc_data.loc_type].append(loc_data)

            answer_long += loc_data.get_answer_mode_long

        if all_locations:
            await db.execute(
                'UPDATE loc SET status = $1, cycle = cycle + 1 WHERE code = any($2::text[])',
                ["⚡", [loc.code for loc in all_locations]]
            )

        answer_short += '{}{}{}\n'.format(
            '\n'.join([l.get_answer for l in sorted(lt['🏷'], key=lambda i: i.lvl)]) + '\n\n' if lt.get('🏷') else '',
            '\n'.join([l.get_answer for l in sorted(lt['📦'], key=lambda i: i.lvl)]) + '\n\n' if lt.get('📦') else '',
            '\n'.join([l.get_answer for l in sorted(lt['🎖'], key=lambda i: i.lvl)]) if lt.get('🎖') else '',
        )

        ending = get_ending(date, mid)

        answer_long += ending
        answer_short += ending

        # Notifications
        chats: List[ChatInfo] = await db.fetch_orm(ChatInfo, BRIEF_NTF_REQ)
        if not chats:
            return

        for chat in chats:
            try:
                await bot.send_message(chat.id, answer_short if chat.brief_mode else answer_long)

            except Exception:
                logging.error(traceback.format_exc())

    client.start()
    client.run_until_disconnected()


def get_date_and_message_id(message: Message):
    if hasattr(message, 'fwd_from') and hasattr(message.fwd_from, 'channel_post'):
        raw_date = message.fwd_from.date
        mid = message.fwd_from.channel_post

    else:
        raw_date = message.date
        mid = message.id

    date = str(raw_date.strftime('%Y-%m-%d %H:%M:%S'))

    return raw_date, date, mid


def get_ending(date: str, mid: int):
    return '[{}]'.format(f'<a href="https://t.me/ChatWarsDigest/{mid}">{date}</a>')


if __name__ == '__main__':
    # Process Name (for Linux)
    if sys.platform == 'linux':
        import ctypes

        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, 'B', 0, 0, 0)

    # Set Logging
    bot_logging.set_logging(config.debug, 'logs/brief.log')

    main()
