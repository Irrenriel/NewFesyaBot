from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import UserData, AL_GET_GUILD_REQ
from src.content.texts.alliance_txt import NO_AL_WELCOME, ALLIANCE_MAIN_PAGE


async def alliance_main_menu(mes: Message, db: PostgreSQLDatabase, user: UserData):
    if user.lvl < 15:
        await mes.answer('Извини, но ты пока маловат уровнем и без гильдии.\nТебе тут делать пока нечего!😊')
        return

    if user.guild_tag == 'None':
        await mes.answer('Для участвия в альянсах тебе как минимум нужна гильдия.\nОбнови /hero если уже состоишь.')
        return

    alliance = await db.fetch(AL_GET_GUILD_REQ, [user.guild_tag], one_row=True)
    if not alliance:
        kb = InlineKeyboard(Call('❇️Зарегистрировать', 'al:new'), Call('❌Закрыть', 'cancel'))
        await mes.answer(NO_AL_WELCOME, reply_markup=kb)
        return

    pool = ('al_name', 'al_code', 'al_owner', 'al_leader', 'n_members', 'n_guilds', 'al_guilds')
    data = {i: alliance.get(i) for i in pool}

    await mes.answer(ALLIANCE_MAIN_PAGE.format(**data, main_last_update='', roster_last_update=''))
