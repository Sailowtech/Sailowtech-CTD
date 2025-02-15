from enum import StrEnum, Enum, auto
from peewee import *

class Sensor(StrEnum):
    """
    Types of all the available sensors. Can then be used in other parts of the software, for example in the config file parsing.
    """
    BLUEROBOTICS_BAR30_DEPTH = auto()
    ATLAS_EZO_CONDUCTIVITY = auto()
    ATLAS_EZO_DO = auto()
    ATLAS_EZO_TEMP = auto()
    MOCK_SENSOR = auto()


class SensorTypeField(Field):
    field_type = 'sensor_type'

    def db_value(self, value):
        return value.value

    def python_value(self, value):
        return Sensor(value)
