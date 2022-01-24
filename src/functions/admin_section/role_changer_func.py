from aiogram.types import Message

from config import ADMINS_ID
from resources.tools.database import PostgreSQLDatabase
from src.content import users, UserData, banned_users, BANNED_MAIN_REQ


async def reg_as(mes: Message, db: PostgreSQLDatabase):
    role = mes.get_args()
    if not role.isdigit():
        await mes.answer('Error: Incorrect Syntax!')
        return

    man: UserData = await users.select_id(mes.reply_to_message.from_user.id)
    if not man:
        await mes.answer('Error: Not In Database!')
        return

    await users.change_role(db, int(role), man)
    await mes.answer('Success: Done!')


async def ban(mes: Message, db: PostgreSQLDatabase):
    target = mes.get_args()
    if not target and mes.reply_to_message:
        uid = [mes.reply_to_message.from_user.id] if mes.reply_to_message.from_user.id not in ADMINS_ID else []

    elif target and target.isdigit():
        uid = [int(target)] if int(target) not in ADMINS_ID else []

    else:
        uid = [
            x.get('id') for x in await db.fetch('SELECT id FROM users WHERE guild_tag = $1', [target])
            if x.get('id') not in ADMINS_ID
        ]
        if not uid:
            await mes.answer('Error: No Guild!')
            return

    if uid:
        await db.execute(
            'INSERT INTO banned_users (id) VALUES ($1) ON CONFLICT DO NOTHING', [[i,] for i in uid], many=True
        )

        await banned_users.update(await db.fetch(BANNED_MAIN_REQ))
        await mes.answer('Success: Done!')

    else:
        await mes.answer('Error: No Users To Ban!')


async def unban(mes: Message, db: PostgreSQLDatabase):
    target = mes.get_args()
    if not target and mes.reply_to_message:
        uid = [mes.reply_to_message.from_user.id] if mes.reply_to_message.from_user.id not in ADMINS_ID else []

    elif target and target.isdigit():
        uid = [int(target)] if int(target) not in ADMINS_ID else []

    else:
        uid = [
            x.get('id') for x in await db.fetch('SELECT id FROM users WHERE guild_tag = $1', [target])
            if x.get('id') not in ADMINS_ID
        ]
        if not uid:
            await mes.answer('Error: No Guild!')
            return

    if uid:
        await db.execute('DELETE FROM banned_users WHERE id = any($1::integer[])', [uid])
        await banned_users.update(await db.fetch(BANNED_MAIN_REQ))
        await mes.answer('Success: Done!')

    else:
        await mes.answer('Error: No Users To Unban!')