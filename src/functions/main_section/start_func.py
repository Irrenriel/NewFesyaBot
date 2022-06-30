import asyncio
import re
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import config
from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from src.content import START_MAIN_MENU_TEXT, start_kb, HERO_PARSE, REG_NEW_USER_REQ, UPDATE_USER_REQ, UsersCash, \
    MAIN_REQ, UserData


async def start(mes: Message, state: FSMContext):
    # If already registered
    await mes.answer(START_MAIN_MENU_TEXT, reply_markup=start_kb())
    await state.reset_state()
    await state.finish()


async def start_new(mes: Message):
    await mes.answer(
        'Требуется пройти регистрацию!\n(Пришли /hero из @ChatWarsBot)', reply_markup=ReplyKeyboardRemove()
    )
    await StateOn.Registration.set()


async def hero_insert(mes: Message, state: FSMContext, db: PostgreSQLDatabase, user: UserData):
    first_time = True if not user else False

    if mes.from_user.username is None:
        await mes.answer('У вас отсутствует @username. Установите его в настройках Telegram!')
        return

    # Is this /hero
    if mes.forward_from is None or mes.forward_from.id != config.CW_BOT_ID or "🎉Достижения: /ach" not in mes.text:
        await mes.answer('Требуется переслать /hero из @ChatWarsBot!')
        return

    # Is this NEW /hero
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старый /hero. Пришли новый!')
        return

    # Adding new user
    if await new_user_register(mes, db, first_time=first_time) is None:
        await mes.answer('Этот /hero с ошибками! Не удаётся получить информацию! Обратитесь к @Wolftrit.')
        return

    if first_time:
        await mes.answer(f'Добро пожаловать, {mes.from_user.username}!')
        await start(mes, state)

    else:
        await mes.answer('Информация успешно обновлена!')


async def new_user_register(mes: Message, db: PostgreSQLDatabase, first_time: bool = True):
    # Collecting data
    parse = re.search(HERO_PARSE, mes.text)
    if not parse:
        return

    u = mes.from_user

    lvl = int(parse.group('lvl'))
    nickname = parse.group('nickname')

    m_class, s_class = await get_class(parse.group('class'))
    if not m_class:
        return

    castle = await get_castle(parse.group('castle'))
    guild_tag = parse.group('guild_tag') if parse.group('guild_tag') else 'None'

    if first_time:
        await db.execute(REG_NEW_USER_REQ, [u.id, u.username, nickname, lvl, m_class, s_class, guild_tag, castle])
        await UsersCash.add_new_user(db, u.id)

    else:
        await db.execute(UPDATE_USER_REQ, [u.username, nickname, lvl, m_class, s_class, guild_tag, castle, u.id])
        await UsersCash.update(await db.fetch(MAIN_REQ))

    return True


async def get_class(x):
    d = {'🐣': -2, '🏛': -1, '⚔️': 1, '🏹': 2, '🛡': 3, '🩸': 4, '⚒': 5, '⚗️': 6, '📦': 7, '🎩': 8}
    for emj in d:
        if x.startswith(emj):
            m_class = d.get(emj, 0)
            if not m_class:
                return 0, 0

            x = x.replace(emj, '')
            break

    else:
        return 0, 0

    if x:
        for emj in d:
            if x.startswith(emj):
                s_class = d.get(emj, 0)
                break

        else:
            s_class = 0

    else:
        s_class = 0

    return m_class, s_class


async def get_castle(x):
    return {'☘️': 1, '🍁': 2, '🍆': 3, '🦇': 4, '🖤': 5, '🌹': 6, '🐢': 7}.get(x, 0)
