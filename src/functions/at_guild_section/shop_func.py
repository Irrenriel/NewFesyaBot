import random
import re

from aiogram.types import Message

from resources.models import client
from resources.tools.telethon import TelethonQueue
from src.content import UserData, GOLD_TEXT
from src.functions.admin_section.settings_func import delete_message_with_notification


async def gold_func(mes: Message, user: UserData):
    if user.guild_tag != 'AT':
        return

    if not TelethonQueue.get_status():
        m = await mes.answer('<b>[❌] Аккаунт занят. Повторите позже.</b>')
        await delete_message_with_notification(mes, m, 5, 5)
        return

    with TelethonQueue() as tq:
        load = await mes.answer('<b>[⏳] Запрашиваю, подожди.</b>')
        answer = await client.shop_gold_method()

    mana = re.search(r'\w*/\w+', answer['/ws_MYdnt']).group(0)
    cost = re.search(r'Steel mold, 15💧 (\d+)', answer['/ws_MYdnt_stand']).group(1)
    rand_price = str(random.randint(1, 999))
    open = 'Открыто✅' if 'Studio is открыто.' in answer['/ws_MYdnt'] else 'Закрыто🚫'

    await load.edit_text(GOLD_TEXT.format(cost, rand_price, open, mana))


# /open_shop
async def open_shop_func(mes: Message, user: UserData):
    if user.guild_tag != 'AT':
        return

    if not TelethonQueue.get_status():
        m = await mes.answer('<b>[❌] Аккаунт занят. Повторите позже.</b>')
        await delete_message_with_notification(mes, m, 5, 5)
        return

    with TelethonQueue() as tq:
        load = await mes.answer('<b>[⏳] Попробую открыть, подожди.</b>')
        answer = await client.conversation('/myshop_open', float(str(random.uniform(1, 3))[0:4]))

    txt = '<b>[✅] Открыто! Заходи!</b>' if "It's OPEN now." in answer else '<b>[❌] Провал! Требуется подождать...</b>'
    await load.edit_text(txt)


# /change_cost
async def change_cost_func(mes: Message, regexp_command, user: UserData):
    if user.guild_tag != 'AT':
        return

    if not TelethonQueue.get_status():
        m = await mes.answer('<b>[❌] Аккаунт занят. Повторите позже.</b>')
        await delete_message_with_notification(mes, m, 5, 5)
        return

    with TelethonQueue() as tq:
        load = await mes.answer('<b>[⏳] Меняю цену, подожди.</b>')

        cc = regexp_command.group(1)
        if not 1 < int(regexp_command.group(1)) < 1000:
            await load.edit_text('<b>[❌] Недоступная цена.</b>')
            return

        answer = await client.conversation(f'/s_695_add 27 {cc}', float(str(random.uniform(1, 3))[0:4]))

    if 'Steel mold, 15💧 {}💰'.format(cc) in answer:
        txt = '<b>[✅] Успех! Установленная цена {}💰!</b>'.format(cc)

    else:
        txt = '<b>[❌] Провал! Что-то не так.</b>'

    await load.edit_text(txt)
