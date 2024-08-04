from enum import StrEnum


class ValueIDs(StrEnum):
    TIMESTAMP = "timestamp"
    DATE = "date"
    PRESSURE_MBA = "pressure (mba)"
    DEPTH_METERS = "calculated depth (m)"
    TEMPERATURE = "temperature (°C)"
