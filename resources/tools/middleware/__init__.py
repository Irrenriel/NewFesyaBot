from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Throttled

from config import config
from resources.tools.database import PostgreSQLDatabase
from src.content import UsersCash, AdvUsersCash, ACTIVITY_LOGGING_REQ_INSERT, BannedUsersCash


class Middleware(BaseMiddleware):
    def __init__(self, db: PostgreSQLDatabase):
        self.db = db

        self.rate_limit = 5
        self.prefix = 'antiflood'

        super(Middleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['db'] = self.db
        data['user'] = await UsersCash.select_id(message.from_user.id)
        data['adv_user'] = await self.auc.select_id(message.from_user.id)

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['db'] = self.db
        data['user'] = await UsersCash.select_id(callback_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(callback_query.from_user.id)

    async def on_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        data['db'] = self.db
        data['user'] = await UsersCash.select_id(inline_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(inline_query.from_user.id)


class BanMiddleware(BaseMiddleware):
    """ Ban checking and logging in DB"""
    def __init__(self, db: PostgreSQLDatabase):
        self.db = db

        super(BanMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message):
        if message.from_user.id not in config.ADMINS_ID:
            await self.add_log(message, f'MSG: {message.text}')

        if message.from_user.id in await BannedUsersCash.get_storage():
            raise CancelHandler()

    async def on_process_callback_query(self, callback_query: types.CallbackQuery):
        if callback_query.from_user.id not in config.ADMINS_ID:
            await self.add_log(callback_query, f'CLB: {callback_query.data}')

        if callback_query.from_user.id in await BannedUsersCash.get_storage():
            raise CancelHandler()

    async def on_process_inline_query(self, inline_query: types.InlineQuery):
        if inline_query.from_user.id not in config.ADMINS_ID:
            await self.add_log(inline_query, f'INL: {inline_query.query}')

        if inline_query.from_user.id in await BannedUsersCash.get_storage():
            raise CancelHandler()

    async def add_log(self, update, data: str):
        if update.from_user.username:
            username = update.from_user.username
        else:
            username = update.from_user.first_name + ' FN'

        await self.db.execute(ACTIVITY_LOGGING_REQ_INSERT, [update.from_user.id, username, data])
