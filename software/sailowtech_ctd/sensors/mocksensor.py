import smbus2 as smbus
import random

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.sensors.types import Sensor


class MockSensor(GenericSensor):

    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min: int, max: int):
        self.min = min
        self.max = max
        super().__init__(brand, sensor_type, name, address)

    def init(self, bus: smbus.SMBus):
        return True

    def measure_value(self, bus: smbus.SMBus):
        return random.uniform(self.min, self.max)