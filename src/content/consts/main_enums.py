from enum import Enum


class Castles(Enum):
    OPLOT = '☘'
    AMBER = '🍁'
    FERMA = '🍆'
    NIGHT = '🦇'
    SKALA = '🖤'
    DAWN = '🌹'
    TORTUGA = '🐢'
    ERROR = 'ERROR'


class Roles(Enum):
    ADMIN = -1
    COMMON = 1
    OFFICER = 2
    COMMANDER = 3
    ALLIANCE_LEADER = 4


class Classes(Enum):
    # Squair
    KNIGHT = '⚔️'
    RANGER = '🏹'
    SENTINEL = '🛡'
    BERSERK = '🩸'

    # Master
    BLACKSMITH = '⚒'
    ALCHEMIST = '⚗️'
    COLLECTOR = '📦'
    NOBLE = '🎩'