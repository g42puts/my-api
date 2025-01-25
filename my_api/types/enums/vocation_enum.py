from enum import Enum


class TibiaVocationEnum(Enum):
    KNIGHT = 1
    ELITE_KNIGHT = 2
    PALADIN = 3
    ROYAL_PALADIN = 4
    DRUID = 5
    ELDER_DRUID = 6
    SORCERER = 7
    MASTER_SORCERER = 8
    NONE = 9


TibiaVocationEnum = Enum('TibiaVocationEnum', {v.name: v for v in TibiaVocationEnum})
