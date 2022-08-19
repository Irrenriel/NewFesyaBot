import re
from datetime import timedelta, datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import config
from resources.tools.database import PostgreSQLDatabase
from resources.tools.states import StateOn
from src.content import AdvUserData, ADV_GUILD_MENU_TEXT, adv_guild_kb, ADV_GUILD_WELCOME_TEXT, HERO_PARSE, \
    RegisterUser, ADV_GUILD_WELCOME2_TEXT, UserData
from src.functions import hero_insert


async def adv_guild_func(mes: Message, adv_user: AdvUserData):
    if adv_user:
        await mes.answer(ADV_GUILD_MENU_TEXT, reply_markup=adv_guild_kb())

    await mes.answer(ADV_GUILD_WELCOME_TEXT, reply_markup=ReplyKeyboardRemove())
    await StateOn.AdvStart.set()


async def adv_guild_registration(mes: Message, db: PostgreSQLDatabase, state: FSMContext, user: UserData):
    if mes.from_user.username is None:
        await mes.answer('У вас отсутствует @username. Установите его в настройках Telegram!')
        return

    # Is this /hero
    if not mes.forward_from or mes.forward_from.id != config.CW_BOT_ID or "🎉Достижения: /ach" not in mes.text:
        await mes.answer('Требуется переслать /hero из @ChatWarsBot!')
        return

    # Is this NEW /hero
    if not datetime.now() - mes.forward_date < timedelta(seconds=30):
        await mes.answer('Слишком старый /hero. Пришли новый!')
        return

    if await hero_insert(mes, state, db, user) is None:
        await mes.answer('Этот /hero с ошибками! Не удаётся получить информацию! Обратитесь к @Wolftrit.')
        return

    # All is OK
    await mes.answer(ADV_GUILD_WELCOME2_TEXT.format(mes.from_user.username))
    await mes.answer(ADV_GUILD_MENU_TEXT, reply_markup=adv_guild_kb())
    await state.finish()
