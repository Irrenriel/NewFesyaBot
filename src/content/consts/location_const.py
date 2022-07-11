from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LocTypes(Enum):
    ALLIANCE = -1
    RUINS = 1
    MINE = 2
    FORT = 3


LOC_TYPES_BY_NAME = {'Ruins': '🏷', 'Mine': '📦', 'Fort': '🎖', 'Tower': '🎖', 'Outpost': '🎖'}

LOC_TYPES_ENUM = {
    'Ruins': LocTypes.RUINS, 'Mine': LocTypes.MINE, 'Fort': LocTypes.FORT, 'Tower': LocTypes.FORT,
    'Outpost': LocTypes.FORT
}

GET_LOC_TYPE_EMOJI = {LocTypes.RUINS: '🏷', LocTypes.MINE: '📦', LocTypes.FORT: '🎖', LocTypes.ALLIANCE: '🎪'}

STATUS_HEADQUARTERS_DICT = {
    'easily defended': '👌🛡',
    'easily breached': '😎⚔',
    'breached': '⚔',
    'defended successfully': '🛡',
    'closely defended': '⚡🛡',
    'closely breached': '⚡⚔'
}

STATUS_LOCATIONS_DICT = {
    '. Easy win:': '😎⚔',
    ':': '⚔',
    '. Massacre:': '⚡⚔',
    'easily protected': '👌🛡',
    'protected': '🛡',
    'closely protected': '⚡🛡'
}

FORBIDDEN_CLASSES = {
    'Sentinel': '🛡'
}


class LocInfoData(BaseModel):
    code: str
    name: str
    lvl: int
    type: LocTypes
    conqueror: str
    cycle: int
    status: str


@dataclass
class LocHistoryData:
    date: datetime
    url: int
    text: str


@dataclass
class LocGuildInfo:
    guild_tag: str
    guild_emoji: str


@dataclass
class HQParsingData:
    code: str
    name: str
    status: str
    stock: str
    glory: str

    raw_date: datetime = None
    date: str = None
    message_id: int = None

    atk_answer = ''
    def_answer = ''

    own = ''
    breach = ''

    def hq_date(self, raw_date: datetime, mid: int):
        self.raw_date = raw_date
        self.date = str(raw_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.message_id = mid

    @property
    def hq_url(self):
        return '<a href="https://t.me/share/url?url=/l_info%20{}">🎪{}</a>'.format(self.code, self.name)

    def breaching_raider_log(self, raider_code: str, ):
        return raider_code, self.raw_date, self.message_id, f'<b>🎪{raider_code} ⚔➡ 🎪{self.name}</b>'

    def breached_hq_log(self, raiders: set):
        txt = f'<b>🎪{self.name}[{self.status}]\n⬆⚔ 🎪{",🎪".join(raiders)}</b>'
        return self.code, self.raw_date, self.message_id, txt

    @property
    def get_answer_mode_long(self):
        return f'<b>{self.own}{self.hq_url} [{self.status}]</b>\n{self.breach}{self.atk_answer}{self.def_answer}\n'

    @property
    def get_answer_mode_short(self):
        return f'<b>{self.own}{self.hq_url} [{self.status}]</b>\n'


@dataclass
class LocParsingData:
    code: str
    name: str
    lvl: int
    status: str
    type: LocTypes
    new_conqueror: str
    prev_conqueror: str = 'Forbidden Clan'

    def_status: str = None
    atk_status: str = None

    raw_date: datetime = None
    date: str = None
    message_id: int = None

    atk_answer = ''
    def_answer = ''

    own = ''
    new_conqueror_code = ''

    new_location: bool = False

    def loc_date(self, raw_date: datetime, mid: int):
        self.raw_date = raw_date
        self.date = str(raw_date.strftime('%Y-%m-%d %H:%M:%S'))
        self.message_id = mid

    @property
    def loc_conquest_log(self):
        x = f'<b>{LOC_TYPES_BY_NAME.get(self.name.split(" ")[-1])}{self.name} lvl.{self.lvl}[✅🚩]</b>'
        return self.new_conqueror_code, self.raw_date, self.message_id, x

    @property
    def loc_failed_defend_log(self):
        x = f'<b>{self.loc_type}{self.name} lvl.{self.lvl}[🚫🚩]</b>'
        return self.new_conqueror_code, self.raw_date, self.message_id, x

    @property
    def get_answer(self):
        return f'<b>{self.own}{self.loc_type}{self.name_lvl} [{self.status}]</b>'

    @property
    def get_new_loc_answer(self):
        return f'<b>{self.own}{self.loc_type}{self.name_lvl}</b>'

    @property
    def get_answer_mode_long(self):
        return '<b>{}{}{} [{}]{}</b>\n{}{}\n'.format(
            self.own, self.loc_type, self.name_lvl, self.status, self.new_owner, self.atk_answer, self.def_answer
        )

    @property
    def loc_type(self):
        return LOC_TYPES_BY_NAME.get(self.name.split(' ')[-1])

    @property
    def new_owner(self):
        return f'\n➕🚩[{self.new_conqueror}]' if self.new_conqueror else ''

    @property
    def name_lvl(self):
        return f'{self.name} lvl.{self.lvl}'

    @property
    def get_none_code(self):
        return f'NoneCode({self.name} lvl.{self.lvl})'
