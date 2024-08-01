from dataclasses import dataclass
from enum import Enum, auto


class SensorBrand(Enum):
    Atlas = auto()
    BlueRobotics = auto()


class SensorType(Enum):
    # Atlas
    DISSOLVED_OXY = auto()
    CONDUCTIVITY = auto()
    DISSOLVED_OXY_TEMP = auto()
    # Blue robotics
    DEPTH = auto()


class GenericSensor:
    class Commands(Enum):
        ...
    
    def __init__(self, sensor_type: SensorType, name: str, address: int, brand: SensorBrand, min_delay: float = 1):
        self.sensor_type: SensorType = sensor_type
        self.brand: SensorBrand = brand

        self.name: str = name
        self.addr: int = address

        self.min_delay: float = min_delay
        self.last_read: float = 0.

    def read_value(self):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'name="{self.name}", ' \
               f'address={hex(self.addr)}' \
               f')'

    def __repr__(self):
        return self.__str__()
