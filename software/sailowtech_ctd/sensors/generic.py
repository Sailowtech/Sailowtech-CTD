from enum import Enum, auto

import smbus2 as smbus
from .types import Sensor

class SensorBrand(Enum):
    Atlas = auto()
    BlueRobotics = auto()
    MockBrand = auto()

class GenericSensor:
    class Commands(Enum):
        ...

    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min_delay: float = 1):
        self.brand: SensorBrand = brand
        self.sensor_type: Sensor = sensor_type

        self.name: str = name
        self.addr: int = address

        self.min_delay: float = min_delay
        self.last_read: float = 0.

    def init(self, bus: smbus.SMBus):
        ...

    def calibrate(self, bus: smbus.SMBus):
        ...

    def measure_value(self, bus: smbus.SMBus):
        ...

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'name="{self.name}", ' \
               f'address={hex(self.addr)}' \
               f'brand={self.brand}' \
               f'type={self.sensor_type}' \
               f')'

    def __repr__(self):
        return self.__str__()
