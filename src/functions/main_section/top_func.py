from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import TopResult, UsersCash, UserData
from src.content.consts.main_enums import GET_CLASS_EMOJI


async def top1(mes: Message, db: PostgreSQLDatabase):
    results = [TopResult(**r) for r in await db.fetch('SELECT uid, count FROM location_top')]
    text = '<u><b>🗺Топ сыщиков локаций:</b></u>\n\n'

    if results:
        num = 1
        for result in results:
            user: UserData = await UsersCash.select_id(result.uid)
            if not user:
                continue

            class_emoji = GET_CLASS_EMOJI.get(user.main_class)
            text += f'<b>{num}) {class_emoji}[{user.guild_tag}]{user.nickname} — {result.count}</b>\n'

    else:
        text += 'Пусто'

    await mes.answer(text)


async def top2(mes: Message, db: PostgreSQLDatabase):
    results = [TopResult(**r) for r in await db.fetch('SELECT uid, count FROM location_top')]
    text = '<u><b>🗺Топ гильдий-сыщиков локаций:</b></u>\n\n'

    if results:
        guilds = {}

        for result in results:
            user: UserData = await UsersCash.select_id(result.uid)
            if not user or not user.guild_tag:
                continue

            guilds[user.guild_tag] = guilds.setdefault(user.guild_tag, 0) + result.count

        if guilds:
            for i, guild in enumerate(list(sorted(guilds.items(), key=lambda item: item[1])), start=1):
                text += f'<b>{i}) [{guild[0]}] — {guild[1]}</b>\n'

        else:
            text += 'Пусто'

    else:
        text += 'Пусто'

    await mes.answer(text)
