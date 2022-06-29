from typing import Union

from aiogram.types import Message, CallbackQuery

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import UserData, AL_GET_ALLIANCE_BY_GUILD_REQ, NO_AL_WELCOME
from src.functions.alliance_section.alliance_base_helpful_func import alliance_main_menu_text


async def alliance_main_menu(mes: Union[Message, CallbackQuery], db: PostgreSQLDatabase, user: UserData):
    func = mes.answer if isinstance(mes, Message) else mes.message.edit_text

    if user.lvl < 15:
        await func('Извини, но ты пока маловат уровнем и без гильдии.\nТебе тут делать пока нечего!😊')
        return

    if user.guild_tag == 'None':
        await func('Для участвия в альянсах тебе как минимум нужна гильдия.\nОбнови /hero если уже состоишь.')
        return

    alliance = await db.fetch(AL_GET_ALLIANCE_BY_GUILD_REQ, [user.guild_tag], one_row=True)

    if not alliance:
        kb = InlineKeyboard(Call('❇️Зарегистрировать', 'al:new'), Call('❌Закрыть', 'cancel'))
        await func(NO_AL_WELCOME, reply_markup=kb)
        return

    await alliance_main_menu_text(mes, db, user)
