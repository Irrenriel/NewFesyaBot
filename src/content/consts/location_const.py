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

GET_LOC_TYPE_EMOJI = {LocTypes.RUINS: '🏷', LocTypes.MINE: '📦', LocTypes.FORT: '🎖'}

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
