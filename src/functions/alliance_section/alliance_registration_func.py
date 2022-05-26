from datetime import datetime, timedelta
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from src.content.texts.alliance_txt import REG_AL_WELCOME, REG_GET_CODE, REG_GET_MAIN
from src.content import TempAllianceCash, AL_MAIN_PARSE


async def alliance_new_reg(call: CallbackQuery, state: FSMContext):
    await state.reset_data()
    await call.message.edit_text(REG_AL_WELCOME)
    await StateOn.AllianceGetCode.set()


async def alliance_get_code(mes: Message, db: PostgreSQLDatabase, state: FSMContext):
    # IF NOT CORRECT OR NOT EXIST
    if len(mes.text) != 6 or not await db.fetch('SELECT * FROM loc WHERE code = $1', [mes.text], one_row=True):
        await mes.answer('Неверный код! Попробуйте ещё...')
        return

    # IF ALREADY REGISTERED
    if await db.fetch('SELECT * FROM alliance_hq WHERE al_code = $1', [mes.text], one_row=True):
        await mes.answer('Данный альянс уже зарегистрирован! Выясняйте кем или пишите в поддержку.')
        return

    await state.update_data(al_code=mes.text)
    await mes.answer(REG_GET_CODE)
    await StateOn.AllianceGetMenu.set()


async def alliance_get_main(mes: Message, db: PostgreSQLDatabase, state: FSMContext):
    parse = re.match(AL_MAIN_PARSE, mes.text)
    if parse is None:
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    data = await state.get_data()

    parsing_data = parse.groupdict()

    al = await db.fetch('SELECT name FROM loc WHERE code = $1', [data['al_code']], one_row=True)

    if not al or al['name'] != parsing_data['name']:
        await mes.answer('Имя альянса не совпадает. Чужой Альянс кидаешь!!1!')
        return

    await state.update_data(parsing_data)
    print(await state.get_data())
    return

    await TempAllianceCash.add_main(
        mes.from_user.id,
        name, owner, int(n_guilds), int(n_peoples), int(b_pogs), int(b_money), int(stock), int(glory), str(mes)
    )
    await mes.answer(REG_GET_MAIN)
    await StateOn.AllianceGetRoster.set()


async def alliance_get_roster(mes: Message, db: PostgreSQLDatabase):
    parse = re.findall(r'(.+)\[(.+)\](.+)', mes.text.replace('📋Roster:\n', ''))
    if parse is None:
        await mes.answer('Неверный формат🤚\nВ случае ошибки обратитесь к администратору.')
        return

    # IF NOt NEW MESSAGE
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старое сообщение. Пришли новое!')
        return

    l_parse = [x[1] for x in parse]
    if len(l_parse) != await TempAllianceCash.get_num_guilds(mes.from_user.id):
        await mes.answer('Количество гильдий не совпадает. Чужой Альянс кидаешь!!1!')
        return

    await TempAllianceCash.add_roster(mes.from_user.id, l_parse, str(mes))

    # alliance = await TempAllianceCash.get_data(mes.from_user.id)
    # await db.execute(REG_NEW_ALLIANCE, [])