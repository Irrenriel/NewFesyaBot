from aiogram.types import Message, CallbackQuery

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import HELP_NEW_CHAT_ID_TEXT, SETTINGS_GET_CHAT, SETTINGS_TEXT
from src.content.consts.main_resources import ChatInfo


async def new_chat_found(mes: Message, db: PostgreSQLDatabase):
    if await db.fetch('SELECT * FROM chats WHERE id = $1', [mes.chat.id], one_row=True):
        return

    await db.execute('INSERT INTO chats (id) VALUES ($1)', [mes.chat.id])
    await mes.answer(HELP_NEW_CHAT_ID_TEXT)


async def settings(mes: Message, db: PostgreSQLDatabase):
    req = await db.fetch(SETTINGS_GET_CHAT, [mes.chat.id], one_row=True)

    if not req:
        await db.execute('INSERT INTO chats (id) VALUES ($1)', [mes.chat.id])
        req = await db.fetch(SETTINGS_GET_CHAT, [mes.chat.id], one_row=True)

    chat = ChatInfo(**req)
    d = {False: '❌', True: '✅'}

    answer = SETTINGS_TEXT.format(
        d.get(chat.new_loc_ntf), d.get(chat.delete_loc_ntf), d.get(chat.brief_log), d.get(chat.brief_mode)
    )

    await mes.answer(answer, reply_markup=settings_keyboard(chat))


def settings_keyboard(chat: ChatInfo):
    new_loc_ntf = Call('Вкл✅', 'nln:off') if chat.new_loc_ntf else Call('Откл❌', 'nln:on')
    delete_loc_ntf = Call('Вкл✅', 'dln:off') if chat.delete_loc_ntf else Call('Откл❌', 'dln:on')
    brief_log = Call('Вкл✅', 'brf:off') if chat.brief_log else Call('Откл❌', 'brf:on')
    brief_mode = Call('Вкл✅', 'brfm:off') if chat.brief_mode else Call('Откл❌', 'brfm:on')
    return InlineKeyboard(new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, Call('Закрыть', 's_cancel'), row_width=4)


async def settings_v(call: CallbackQuery, db: PostgreSQLDatabase):
    await call.answer(cache_time=1)

    mode, sw = call.data.split(':')

    modes = {'nln': 'new_loc_ntf', 'dln': 'delete_loc_ntf', 'brf': 'brief_log', 'brfm': 'brief_mode'}
    switch = {'on': True, 'off': False}

    await db.execute(f'UPDATE chats SET {modes.get(mode)} = $1 WHERE id = $2', [switch.get(sw), call.message.chat.id])
    chat = ChatInfo(**(await db.fetch(SETTINGS_GET_CHAT, [call.message.chat.id], one_row=True)))

    d = {False: '❌', True: '✅'}

    answer = SETTINGS_TEXT.format(
        d.get(chat.new_loc_ntf), d.get(chat.delete_loc_ntf), d.get(chat.brief_log), d.get(chat.brief_mode)
    )

    await call.message.edit_text(answer, reply_markup=settings_keyboard(chat))
