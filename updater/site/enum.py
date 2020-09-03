from enum import auto, Enum, IntEnum


class GameVersion(Enum):
    agnostic = auto()
    retail = auto()
    classic = auto()


class AddonVersion(IntEnum):
    release = 3
    beta = 2
    alpha = 1
