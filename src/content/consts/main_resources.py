from dataclasses import dataclass

from aiogram.types import Message
from pydantic import BaseModel


@dataclass
class RegisterUser:
    nickname: str
    lvl: str
    castle: str

    classes: str
    guild_tag: str

    op_castle: int = 0
    m_class: int = 0
    s_class: int = 0

    def get_args_for_new(self, mes: Message):
        return mes.from_user.id, mes.from_user.username, self.nickname, int(self.lvl), self.m_class, \
               self.s_class, self.guild_tag, self.op_castle

    def get_args_for_old(self, mes: Message):
        return mes.from_user.username, self.nickname, int(self.lvl), self.m_class, \
               self.s_class, self.guild_tag, self.op_castle, mes.from_user.id

    def process(self):
        self.get_classes()
        self.get_castle()
        self.get_guild_tag()

    def get_castle(self):
        self.op_castle = {'☘️': 1, '🍁': 2, '🍆': 3, '🦇': 4, '🖤': 5, '🌹': 6, '🐢': 7}.get(self.castle, 0)

    def get_guild_tag(self):
        if not self.guild_tag:
            self.guild_tag = 'None'

    def get_classes(self):
        d = {'🐣': -2, '🏛': -1, '⚔️': 1, '🏹': 2, '🛡': 3, '🩸': 4, '⚒': 5, '⚗️': 6, '📦': 7, '🎩': 8}

        # Main Class
        for emj in d:
            if self.classes.startswith(emj):
                self.m_class = d.get(emj, 0)
                if not self.m_class:
                    self.m_class = self.s_class = 0
                    return

                self.classes = self.classes.replace(emj, '')
                break

        else:
            self.m_class = self.s_class = 0
            return

        # Sub Class
        if not self.classes:
            self.s_class = 0
            return

        for emj in d:
            if self.classes.startswith(emj):
                self.s_class = d.get(emj, 0)
                break

        else:
            self.s_class = 0


class ChatInfo(BaseModel):
    id: int

    new_loc_ntf: bool
    delete_loc_ntf: bool

    brief_log: bool
    brief_mode: bool

    craft_ntf: bool
