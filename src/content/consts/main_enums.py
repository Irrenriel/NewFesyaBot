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