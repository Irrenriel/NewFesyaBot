from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from config import ADMINS_ID
from resources.tools.database import PostgreSQLDatabase
from src.content import UsersCash, AdvUsersCash, ACTIVITY_LOGGING_REQ_INSERT


class Middleware(BaseMiddleware):
    def __init__(self, db: PostgreSQLDatabase, uc: UsersCash, auc: AdvUsersCash):
        self.db = db
        self.uc = uc
        self.auc = auc
        super(Middleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in ADMINS_ID:
            await add_log(self.db, message, 'MSG: ' + message.text)

        data['db'] = self.db
        data['user'] = await self.uc.select_id(message.from_user.id)
        data['adv_user'] = await self.auc.select_id(message.from_user.id)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.from_user.id not in ADMINS_ID:
            await add_log(self.db, callback_query, 'CLB: ' + callback_query.data)

        data['db'] = self.db
        data['user'] = await self.uc.select_id(callback_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(callback_query.from_user.id)

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        # if inline_query.from_user.id not in ADMINS_ID:
        #   await add_log(self.db, inline_query, 'INL: ' + inline_query.query)

        data['db'] = self.db
        data['user'] = await self.uc.select_id(inline_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(inline_query.from_user.id)


async def add_log(db: PostgreSQLDatabase, update, data: str):
    if update.from_user.username:
        username = update.from_user.username
    else:
        username = update.from_user.first_name + ' FN'

    await db.execute(
        ACTIVITY_LOGGING_REQ_INSERT,
        [update.from_user.id, username, data]
    )
