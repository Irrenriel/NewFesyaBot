import logging
import re
from datetime import timedelta, datetime

from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import UserData, Roles, AL_MAIN_PARSE, ALLiANCE_UPDATE_MAIN, UPD_COMPLETE, ALLiANCE_UPDATE_ROSTER
from src.functions.alliance_section.alliance_base_helpful_func import sorting_menu_parse


async def alliance_upd_main(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.role != Roles.ALLIANCE_LEADER:
        return

    alliance = await db.fetch(
        'SELECT al_code, al_name FROM alliance_hq WHERE al_leader = $1', [mes.from_user.id], one_row=True
    )

    if not alliance:
        return

    parse = re.match(AL_MAIN_PARSE, mes.text)
    if not parse:
        logging.info(f'[Alliance Updating Main] {mes.from_user.id}: {mes.text}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    pd = await sorting_menu_parse(parse.groupdict(), mes.text)
    if not pd:
        logging.info(f'[Alliance Updating Main] {mes.from_user.id} ({alliance["al_code"]}): {pd}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    if alliance['al_name'] != pd['al_name']:
        await mes.answer('Имя альянса не совпадает. Чужой Альянс кидаешь!')
        return

    await db.execute(
        ALLiANCE_UPDATE_MAIN,
        [
            pd['n_guilds'], pd['n_members'], pd['al_owner'], pd['al_balance_pogs'], pd['al_balance_money'],
            pd['al_stock'], pd['al_glory'], pd['al_main_raw'], alliance['al_code']
        ]
    )

    await mes.answer(UPD_COMPLETE)


async def alliance_upd_roster(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.role != Roles.ALLIANCE_LEADER:
        return

    alliance = await db.fetch(
        'SELECT al_code, n_guilds FROM alliance_hq WHERE al_leader = $1', [mes.from_user.id], one_row=True
    )

    if not alliance:
        return

    parse = re.findall(r'(.+)\[(.+)\](.+)', mes.text.replace('📋Roster:\n', ''))
    if parse is None:
        logging.info(f'[Alliance Updating Roster] {mes.from_user.id}:\n{mes.text}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    al_guilds = [x[1] for x in parse]

    if len(al_guilds) != int(alliance['n_guilds']):
        logging.info(f'[Alliance Updating Roster] {mes.from_user.id}:\n{mes.text}')
        await mes.answer('Количество гильдий не совпадает. Чужой Альянс кидаешь!')
        return

    await db.execute(ALLiANCE_UPDATE_ROSTER, [al_guilds, mes.text, alliance['al_code']])

    await mes.answer(UPD_COMPLETE)
