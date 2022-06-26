import logging
from datetime import datetime, timedelta
import re
from typing import Dict, Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from src.content.texts.alliance_txt import REG_AL_WELCOME, REG_GET_CODE, REG_GET_MAIN, REG_COMPLETE, ALLIANCE_MAIN_PAGE_LEADER
from src.content import AL_MAIN_PARSE, REG_NEW_ALLIANCE, UserData, AL_GET_ALLIANCE_BY_GUILD_REQ, REG_GUILDS_TO_ALLIANCE
from src.functions.alliance_section.alliance_main_menu_func import alliance_main_menu_text


async def alliance_new_reg(call: CallbackQuery, state: FSMContext):
    await state.reset_data()
    await call.message.edit_text(REG_AL_WELCOME)
    await StateOn.AllianceGetCode.set()


async def alliance_get_code(mes: Message, db: PostgreSQLDatabase, state: FSMContext):
    # IF NOT CORRECT OR NOT EXIST
    if len(mes.text) != 6 or not await db.fetch('SELECT * FROM loc WHERE code = $1', [mes.text], one_row=True):
        logging.info(f'[Alliance Registration #1] {mes.from_user.id}: {mes.text}')
        await mes.answer('Неверный код! Попробуйте ещё...')
        return

    # IF ALREADY REGISTERED
    if await db.fetch('SELECT * FROM alliance_hq WHERE al_code = $1', [mes.text], one_row=True):
        logging.info(f'[Alliance Registration #1] {mes.from_user.id}: {mes.text}')
        await mes.answer('Данный альянс уже зарегистрирован! Выясняйте кем или пишите в поддержку.')
        return

    await state.update_data(al_code=mes.text, al_leader=mes.from_user.id)
    await mes.answer(REG_GET_CODE)
    await StateOn.AllianceGetMenu.set()


async def alliance_get_main(mes: Message, db: PostgreSQLDatabase, state: FSMContext):
    parse = re.match(AL_MAIN_PARSE, mes.text)
    if not parse:
        logging.info(f'[Alliance Registration #2] {mes.from_user.id}: {mes.text}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    data = await state.get_data()
    al = await db.fetch('SELECT name FROM loc WHERE code = $1', [data['al_code']], one_row=True)

    parsing_data = await sorting_menu_parse(parse.groupdict(), mes.text)
    if not parsing_data:
        logging.info(f'[Alliance Registration #2] {mes.from_user.id} ({data["al_code"]}): {parsing_data}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    if not al or al['name'] != parsing_data['al_name']:
        await mes.answer('Имя альянса не совпадает. Чужой Альянс кидаешь!')
        return

    await state.update_data(**parsing_data)

    await mes.answer(REG_GET_MAIN)
    await StateOn.AllianceGetRoster.set()


async def alliance_get_roster(mes: Message, db: PostgreSQLDatabase, user: UserData, state: FSMContext):
    parse = re.findall(r'(.+)\[(.+)\](.+)', mes.text.replace('📋Roster:\n', ''))
    if parse is None:
        logging.info(f'[Alliance Registration #3] {mes.from_user.id}:\n{mes.text}')
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    al_guilds = [x[1] for x in parse]
    data = await state.get_data()

    if len(al_guilds) != int(data['n_guilds']):
        logging.info(f'[Alliance Registration #3] {mes.from_user.id}:\n{mes.text}')
        await mes.answer('Количество гильдий не совпадает. Чужой Альянс кидаешь!')
        return

    await db.execute(
        REG_NEW_ALLIANCE,
        [
            data['al_code'], data['al_leader'], data['al_name'], data['n_guilds'], data['n_members'], data['al_owner'],
            data['al_balance_pogs'], data['al_balance_money'], data['al_stock'], data['al_glory'], al_guilds,
            data['al_main_raw'], mes.text
        ]
    )

    await db.execute(REG_GUILDS_TO_ALLIANCE, [(data['al_code'], tag) for tag in al_guilds], many=True)

    await state.reset_data()
    await mes.answer(REG_COMPLETE)
    await state.finish()

    await alliance_main_menu_text(mes, db, user)


async def sorting_menu_parse(parsing_data: dict, msg: str) -> Optional[Dict]:
    keys = [
        'al_name', 'n_guilds', 'n_members', 'al_owner', 'al_balance_pogs', 'al_balance_money', 'al_stock', 'al_glory'
    ]

    primary_keys = ['al_name', 'al_owner']
    int_keys = ['n_guilds', 'n_members', 'al_balance_pogs', 'al_balance_money', 'al_stock', 'al_glory']

    result = {}

    for key in keys:
        k = parsing_data.get(key)

        if not k and key in primary_keys:
            return

        key_in = key in int_keys
        result[key] = (int(parsing_data[key]) if key_in else parsing_data[key]) if k else (0 if key_in else '')

    else:
        result['al_main_raw'] = msg

    return result
