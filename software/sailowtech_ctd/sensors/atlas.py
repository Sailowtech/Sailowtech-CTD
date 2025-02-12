from enum import StrEnum

import smbus2 as smbus
from atlas_i2c import sensors as atlas_sensors
from atlas_i2c import commands

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.logger import logger
from .types import Sensor

def handle_raspi_glitch(response):  # Maybe useless when using smbus ?
    """
    Change MSB to 0 for all received characters except the first
    and get a list of characters
    NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
    and you shouldn't have to do this!
    """
    return list(map(lambda x: chr(x & ~0x80), list(response)))


class AtlasSensor(GenericSensor):
    def __init__(self, sensor: Sensor, name: str, address: int, min_delay: float = 1):
        super().__init__(SensorBrand.Atlas, sensor, name, address, min_delay)
        self.device = atlas_sensors.Sensor(name, address)

    def init(self, bus: smbus.SMBus):
        self.device.connect()

    def calibrate(self, bus: smbus.SMBus):
        pass

    def measure_value(self, bus: smbus.SMBus) -> float:
        print("Measuring atlas sensor...")
        response = self.device.query(commands.READ)
        if response.status_code == 1:
            return float(response.data.decode("UTF-8"))
        else:
            logger.warning("INVALID RESPONSE RECEIVED")
            return 0