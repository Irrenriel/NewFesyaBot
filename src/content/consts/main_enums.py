from enum import Enum


class Castles(Enum):
    ERROR = 0
    OPLOT = 1
    AMBER = 2
    FERMA = 3
    NIGHT = 4
    SKALA = 5
    RASSVET = 6
    TORTUGA = 7


class Roles(Enum):
    ADMIN = -1
    NONE = 0
    COMMON = 1
    OFFICER = 2
    COMMANDER = 3
    ALLIANCE_LEADER = 4


class Classes(Enum):
    # Chick
    CHICK = -1

    # None
    NONE = 0

    # Squair
    KNIGHT = 1
    RANGER = 2
    SENTINEL = 3
    BERSERK = 4

    # Master
    BLACKSMITH = 5
    ALCHEMIST = 6
    COLLECTOR = 7
    NOBLE = 8


class GMRole(Enum):
    FALSE = 0
    TRUE = 1


ROLES_DICT = {-1: Roles.ADMIN, 1: Roles.COMMON, 2: Roles.OFFICER, 3: Roles.COMMANDER, 4: Roles.ALLIANCE_LEADER}

GET_CLASS_EMOJI = {
    Classes.NONE: '🏛', Classes.CHICK: '🐣', Classes.KNIGHT: '⚔️', Classes.RANGER: '🏹', Classes.SENTINEL: '🛡',
    Classes.BERSERK: '🩸', Classes.BLACKSMITH: '⚒', Classes.ALCHEMIST: '⚗️', Classes.COLLECTOR: '📦',
    Classes.NOBLE: '🎩'
}
