from enum import Enum, auto

import smbus2 as smbus
from .types import Sensor

class SensorBrand(Enum):
    """
    The different brands of the sensors. Some brands have their own protocols, which is why we group them together.
    """
    Atlas = auto()
    BlueRobotics = auto()
    MockBrand = auto()

class GenericSensor:
    class Commands(Enum):
        ...

    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min_delay: float = 1):
        """
        Initialisation of a generic sensor
        :param brand: Brand of the sensor
        :param sensor_type: Type of the sensor
        :param name: Name of the sensor
        :param address: Address of the sensor
        :param min_delay: Minimum delay of the sensor required for measuring
        """
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

    def write_read_command(self, bus: smbus.SMBus) -> bool:
        ...

    def read_result(self, bus: smbus.SMBus) -> float:
        ...

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'name="{self.name}", ' \
               f'address={hex(self.addr)}, ' \
               f'brand={self.brand}, ' \
               f'type={self.sensor_type}, ' \
               f'min_delay={self.min_delay}' \
               f')'

    def __repr__(self):
        return self.__str__()
