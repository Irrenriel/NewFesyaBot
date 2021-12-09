from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class Middleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db
        self.cashes = {}
        super(Middleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data['db'] = self.db

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['db'] = self.db

    async def on_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        data['db'] = self.db