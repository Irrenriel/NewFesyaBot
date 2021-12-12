from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from src.content import UsersCash, AdvUsersCash


class Middleware(BaseMiddleware):
    def __init__(self, db, uc: UsersCash, auc: AdvUsersCash):
        self.db = db
        self.uc = uc
        self.auc = auc
        super(Middleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data['db'] = self.db
        data['user'] = await self.uc.select_id(message.from_user.id)
        data['adv_user'] = await self.auc.select_id(message.from_user.id)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['db'] = self.db
        data['user'] = await self.uc.select_id(callback_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(callback_query.from_user.id)

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        data['db'] = self.db
        data['user'] = await self.uc.select_id(inline_query.from_user.id)
        data['adv_user'] = await self.auc.select_id(inline_query.from_user.id)