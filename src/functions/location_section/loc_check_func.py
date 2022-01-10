from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import UserData, Roles


async def loc_check(mes: Message, db: PostgreSQLDatabase, user: UserData):
    # if user.role != Roles.ADMIN:
    #     if
    pass