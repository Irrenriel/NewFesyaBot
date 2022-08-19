import asyncio
import re
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import config
from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from src.content import START_MAIN_MENU_TEXT, start_kb, HERO_PARSE, REG_NEW_USER_REQ, UPDATE_USER_REQ, UsersCash, \
    MAIN_REQ, UserData, RegisterUser, AdvUsersCash, ADV_MAIN_REQ


async def start(mes: Message, state: FSMContext, user: UserData):
    # If already registered
    await mes.answer(START_MAIN_MENU_TEXT, reply_markup=start_kb(user))
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
        await start(mes, state, user)

    else:
        await mes.answer('Информация успешно обновлена!')


async def new_user_register(mes: Message, db: PostgreSQLDatabase, first_time: bool = True, adv: bool = False):
    # Collecting data
    parse = re.search(HERO_PARSE, mes.text)
    if not parse:
        return

    model = RegisterUser(**parse.groupdict())

    # Get Class and Sub Class
    model.process()
    if not model.m_class:
        return

    if first_time:
        await db.execute(REG_NEW_USER_REQ, model.get_args_for_new(mes))
        await UsersCash.add_new_user(db, mes.from_user.id)

    else:
        await db.execute(UPDATE_USER_REQ, model.get_args_for_old(mes))
        await UsersCash.update(await db.fetch(MAIN_REQ))

    if adv:
        pack_id, quests_pack = QuestsGenerator([mes.from_user.id, 1]).get_pack()

        await db.execute('INSERT INTO quest_packs VALUES ($1, $2)', [pack_id, quests_pack])
        await db.execute('INSERT INTO adv_users (id, avail_quests) VALUES ($1, $2)', [mes.from_user.id, quests_pack])
        await AdvUsersCash.update(await db.fetch(ADV_MAIN_REQ))

    return True
