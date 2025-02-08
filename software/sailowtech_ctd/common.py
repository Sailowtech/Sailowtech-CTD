from enum import StrEnum, Enum, auto


class DataFields(StrEnum):
    TIMESTAMP = "timestamp"
    DATE = "date"
    PRESSURE_MBA = "pressure (mba)"
    DEPTH_METERS = "calculated depth (m)"
    TEMPERATURE = "temperature (°C)"