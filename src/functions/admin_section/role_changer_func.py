from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import users, UserData


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