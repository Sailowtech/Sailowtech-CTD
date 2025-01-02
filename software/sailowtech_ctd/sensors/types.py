from enum import StrEnum, Enum, auto


class SensorTypes(StrEnum):
    DISSOLVED_OXY = auto()
    CONDUCTIVITY = auto()
    DISSOLVED_OXY_TEMP = auto()
    DEPTH = auto()
