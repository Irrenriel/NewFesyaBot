from enum import Enum


class LocTypes(Enum):
    RUINS = 1
    MINE = 2
    FORT = 3
    ALLIANCE = -1


LOC_TYPES = {'Ruins': '🏷', 'Mine': '📦', 'Fort': '🎖', 'Tower': '🎖', 'Outpost': '🎖'}

LOC_TYPES_ENUM = {
    'Ruins': LocTypes.RUINS, 'Mine': LocTypes.MINE, 'Fort': LocTypes.FORT, 'Tower': LocTypes.FORT,
    'Outpost': LocTypes.FORT
}
