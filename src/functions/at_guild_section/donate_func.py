import json
import logging
import random
import re
import traceback

from aiogram.types import Message, ChatPermissions, CallbackQuery

from config import config
from resources.models import client
from resources.tools.database import PostgreSQLDatabase
from src.content import UserData, DONATE_TEXT, donate_kb
from src.functions.admin_section.settings_func import delete_message_with_notification


async def create_donate(mes: Message, regexp_command, db: PostgreSQLDatabase, user: UserData):
    chats = [i['id'] for i in await db.fetch('SELECT id FROM chats WHERE donate_fnc = True')]
    if mes.chat.id not in chats:
        return

    if user.guild_tag != 'AT':
        return

    telethon_queue = await db.fetch('SELECT data_bool FROM settings WHERE var = $1', ['telethon_queue'], one_row=True)
    if not telethon_queue.get('data_bool'):
        m = await mes.answer('<b>[❌] Аккаунт занят. Повторите позже.</b>')
        await delete_message_with_notification(mes, m, 5, 5)
        return

    await db.execute('UPDATE settings SET data_bool = False WHERE var = $1', ['telethon_queue'])

    load = await mes.answer('<b>[⏳] Создаю, подожди.</b>')
    answer = await client.conversation('🏅Герой', float(str(random.uniform(1, 3))[0:4]))

    await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])

    if not answer.startswith('Битва семи замков через'):
        await load.edit_text('<b>[❌] Идёт битва! Невозможно в данный момент!</b>')
        return

    summ = int(regexp_command.group(1))
    gold = int(re.search(r'💰(\d+) ', answer).group(1))

    settings_dict = {'mid': load.message_id, 'cid': load.chat.id, 'sum': int(summ), 'gold': int(gold)}

    await db.execute('UPDATE settings SET data_str = $1 WHERE var = $2', [json.dumps(settings_dict), "donate_json"])
    await db.execute('DELETE FROM donates')

    try:
        txt = DONATE_TEXT.format(**get_donate_txt('<b>Начался сбор суммы!</b>\n', gold, summ))

        await load.edit_text(txt, reply_markup=donate_kb())

        if await mes.bot.set_chat_permissions(mes.chat.id, ChatPermissions.can_pin_messages):
            await mes.bot.pin_chat_message(load.chat.id, load.message_id)

        await mes.bot.send_message(config.KIND_SPY_CHANNEL, txt + '#donate')

    except Exception:
        logging.error(traceback.format_exc())


async def update_donate(call: CallbackQuery, db: PostgreSQLDatabase, user: UserData):
    if user.guild_tag != 'AT':
        return

    dj = await db.fetch('SELECT data_str FROM settings WHERE var = $1', ["donate_json"], one_row=True)
    if not dj or not dj['data.str']:
        await call.message.delete()
        return

    telethon_queue = await db.fetch('SELECT data_bool FROM settings WHERE var = $1', ['telethon_queue'], one_row=True)
    if not telethon_queue.get('data_bool'):
        await call.answer('Аккаунт занят. Повторите позже.', cache_time=3)
        return

    await db.execute('UPDATE settings SET data_bool = False WHERE var = $1', ['telethon_queue'])

    await call.answer('Обновляется, подождите!!', cache_time=3)
    answer = await client.conversation('🏅Герой', float(str(random.uniform(1, 3))[0:4]))

    await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])

    if not answer.message.startswith('Битва семи замков через'):
        await call.answer('Идёт битва! Повторите позже!', cache_time=5)
        return

    dj = json.loads(dj['data.str'])

    gold = int(re.search(r'💰(\d+) ', answer.message).group(1))
    dj['gold'] = gold

    await db.execute('UPDATE settings SET data_str = $1 WHERE var = $2', [json.dumps(dj), "donate_json"])

    donaters = await db.fetch('SELECT name, gold FROM donates ORDER BY -gold')

    try:
        txt = DONATE_TEXT.format(**get_donate_txt('<b>Обновлено!</b>\n', gold, dj['sum'], donaters))
        await call.message.edit_text(txt, reply_markup=donate_kb())

    except Exception:
        logging.error(traceback.format_exc())


async def decline_donate(call: CallbackQuery, db: PostgreSQLDatabase, user: UserData):
    if user.guild_tag != 'AT':
        return

    await db.execute('UPDATE settings SET data_str = $1 WHERE var = $2', ["", "donate_json"])

    try:
        if await call.bot.set_chat_permissions(call.message.chat.id, ChatPermissions.can_pin_messages):
            await call.bot.unpin_chat_message(call.message.chat.id, call.message.message_id)

        await call.message.edit_text('<b>Сбор средств успешно отменён!</b>')

        await call.bot.send_message(config.KIND_SPY_CHANNEL, 'Сбор средств успешно отменён!\n#donate')

    except Exception:
        logging.error(traceback.format_exc())


async def pay_donate(call: CallbackQuery, db: PostgreSQLDatabase, user: UserData):
    if user.guild_tag != 'AT':
        return

    dj = await db.fetch('SELECT data_str FROM settings WHERE var = $1', ["donate_json"], one_row=True)
    if not dj or not dj['data.str']:
        await call.message.delete()
        return

    dj = json.loads(dj[0])

    if dj['gold'] < dj['sum']:
        await call.answer('Недостаточно собранных средств!', cache_time=3)
        return

    telethon_queue = await db.fetch('SELECT data_bool FROM settings WHERE var = $1', ['telethon_queue'], one_row=True)
    if not telethon_queue.get('data_bool'):
        await call.answer('Аккаунт занят. Повторите позже.', cache_time=3)
        return

    await db.execute('UPDATE settings SET data_bool = False WHERE var = $1', ['telethon_queue'])

    await call.answer('Обновляется, подождите!!', cache_time=3)
    answer = await client.conversation('/g_pay', float(str(random.uniform(1, 3))[0:4]))

    parse = re.findall(r'/adv_(\S+) .+💰(\d+) /g_pay', answer.message)
    if not parse:
        await call.answer('Казначей занят!', cache_time=3)
        await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])
        return

    for adv in parse:
        if int(adv[1]) == dj['sum']:
            g_pay = [adv[0]]
            break

    else:
        if sum([int(i[1]) for i in parse]) <= dj['sum']:
            g_pay = [i[0] for i in parse]

        else:
            await call.answer('Не понимаю кого оплачивать:(', cache_time=3)
            await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])
            return

    if not g_pay:
        await call.answer('Не понимаю кого оплачивать:(', cache_time=3)
        await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])
        return

    for pay in g_pay:
        answer = await client.conversation(f'/g_pay {pay}', float(str(random.uniform(1, 3))[0:4]))
        if answer != 'Successfully funded!':
            await call.answer('Казначей занят!', cache_time=3)
            await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])
            return

    await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['telethon_queue'])

    await db.execute('UPDATE settings SET data_str = $1 WHERE var = $2', ["", "donate_json"])

    donaters = await db.fetch('SELECT name, gold FROM donates ORDER BY -gold')

    try:
        txt = DONATE_TEXT.format(
            **get_donate_txt('<b>Сумма собрана! Сбор окончен!</b>\n', dj['gold'], dj['sum'], donaters)
        )

        await call.message.edit_text(txt)

        if await call.bot.set_chat_permissions(call.message.chat.id, ChatPermissions.can_pin_messages):
            await call.bot.unpin_chat_message(call.message.chat.id, call.message.message_id)

        await call.bot.send_message(config.KIND_SPY_CHANNEL, txt + '#donate')

    except Exception:
        logging.error(traceback.format_exc())


def get_donate_txt(done: str = '', gold: int = 0, summ: int = 0, donaters=None):
    return {
        'done': done,
        'gold': str(gold),
        'sum': str(summ),
        'donaters': '\n'.join(
            [f'   {str(i)}) {v["name"]} - {v["gold"]}💰' for i, v in enumerate(donaters, start=1)]
        ) if donaters and isinstance(donaters, list) else ''
    }
