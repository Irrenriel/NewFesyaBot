from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase


async def loc_del(mes: Message, db: PostgreSQLDatabase):
    code = mes.get_args()
    if not code:
        await mes.answer('/l_del [код локации]')
        return

    loc = await db.fetch('SELECT * FROM loc WHERE code = $1 and exist = True', [code], one_row=True)
    if not loc:
        await mes.answer('Невозможно. Такой локации нет в базе.')
        return

    await db.execute(
        'UPDATE loc SET exist = False, death_time = LOCALTIMESTAMP WHERE code = $1', [code]
    )
    await mes.answer(f'Выполнено!')

    # chats = (x[0] for x in mes.db.checkall('SELECT id FROM chats WHERE delete_loc_ntf = 1', []))
    # if not chats:
    #     return
    #
    # answer = f'📣Локация с кодом <code>{code}</code> была удалена!\n\nУдаливший: @{mes.from_user.username}'
    # for chat in chats:
    #     try:
    #         await bot.send_message(chat, answer)
    #         await asyncio.sleep(0.3)
    #     except:
    #         pass