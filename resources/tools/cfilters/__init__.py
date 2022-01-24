__all__ = [
    'Command', 'ChatTypeFilter', 'Text', 'IsReplyFilter', 'RegexpCommandsFilter', 'IsChat', 'IsUser', 'IsForward'
]

# Base Filters Import
from aiogram.dispatcher.filters.builtin import Command, ChatTypeFilter, Text, IsReplyFilter, RegexpCommandsFilter

# Types for creating Custom Filters
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from config import config

from src.content import users as uc


# Creating filters
class IsUser(BoundFilter):
    def __init__(
            self, is_id: int = None, is_admin: bool = None, has_username: bool = None, is_registered: bool = None,
            has_roles: [list, int] = None
    ):
        self.is_id = is_id
        self.is_admin = is_admin
        self.has_username = has_username
        self.is_registered = is_registered
        self.has_roles = has_roles

    async def check(self, update) -> bool:
        user = update.from_user

        # If User`s ID == self.id
        if self.is_id is not None and self.is_id != user.id:
            return False

        # Is User Admin or not Admin
        if self.is_admin is not None:
            if self.is_admin and user.id not in config.ADMINS_ID:
                return False
            elif not self.is_admin and user.id in config.ADMINS_ID:
                return False

        # Is User Has Username
        if self.has_username is not None and user.username is None:
            return False

        # Is User Registered
        if self.is_registered is not None:
            if self.is_registered and not await uc.select_id(user.id):
                return False
            elif not self.is_registered and await uc.select_id(user.id):
                return False

        # Is User Has Role
        if self.has_roles is not None and not await uc.check_role(user.id, self.has_roles):
            return False

        return True


class IsForward(BoundFilter):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def check(self, update: Message) -> bool:
        return update.forward_from and update.forward_from.id == self.chat_id


class IsChat(BoundFilter):
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def check(self, update) -> bool:
        return update.chat.id == self.chat_id