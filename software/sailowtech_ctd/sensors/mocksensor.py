import smbus2 as smbus
import random

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.sensors.types import Sensor


class MockSensor(GenericSensor):

    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min_val: int, max_val: int):
        self.min = min_val
        self.max = max_val
        super().__init__(brand, sensor_type, name, address)

    def init(self, bus: smbus.SMBus):
        return True

    def measure_value(self, bus: smbus.SMBus):
        return random.uniform(self.min, self.max)