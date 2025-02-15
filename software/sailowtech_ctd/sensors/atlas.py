from enum import StrEnum

import smbus2 as smbus
from atlas_i2c import atlas_i2c
from atlas_i2c import commands

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.logger import logger
from .types import Sensor, Metric


def handle_raspi_glitch(response):  # Maybe useless when using smbus ?
    """
    Change MSB to 0 for all received characters except the first
    and get a list of characters
    NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
    and you shouldn't have to do this!
    """
    return list(map(lambda x: chr(x & ~0x80), list(response)))


class AtlasSensor(GenericSensor):
    """
    Class which can be used for all (supported) Atlas Scientific sensors
    """
    def __init__(self, sensor: Sensor, name: str, address: int, min_delay: float):
        """
        Initialise Atlas Scientific sensor
        :param sensor: Type of the sensor
        :param name: Name of the sensor
        :param address: I2C-address of the sensor
        :param min_delay: Minimum delay between write / read required for proper functioning
        """
        match sensor:
            case Sensor.ATLAS_EZO_DO: metric_type = Metric.DISSOLVED_OXYGEN
            case Sensor.ATLAS_EZO_TEMP: metric_type = Metric.TEMPERATURE
            case Sensor.ATLAS_EZO_CONDUCTIVITY: metric_type = Metric.CONDUCTIVITY
            case _: metric_type = None; logger.critical("Implementation missing for Sensor!")
        super().__init__(SensorBrand.Atlas, sensor, name, address, min_delay, metric_type)
        self.device = atlas_i2c.AtlasI2C()
        self.device.set_i2c_address(address)

    def init(self, bus: smbus.SMBus) -> None:
        """
        Initialises the sensor. Currently, does not do anything
        :param bus: SMBus object
        :return: Returns nothing
        """
        pass

    def calibrate(self, bus: smbus.SMBus):
        """
        Calibrate the sensor. Currently, does not do anything
        :param bus: SMBus object
        :return: Returns nothing
        """
        pass

    def write_read_command(self, bus: smbus.SMBus = None) -> bool:
        """
        Write a read command to the device.
        :param bus: Bus device. Not required
        :return: Returns true after sending read command
        """
        self.device.write("R")
        return True

    def read_result(self, bus: smbus.SMBus = None) -> float:
        """
        Read the measured value from device.
        :param bus: Bus device. Not required
        :return: Returns true after sending read command
        """
        result = self.device.read("R")
        if result.status_code == 1:
            return float(result.data.decode("UTF-8"))
        else:
            logger.warning(f"Invalid response received from sensor {self.name}")
            return 0

    def measure_value(self, bus: smbus.SMBus) -> float:
        response = self.device.query(commands.READ)
        if response.status_code == 1:
            return float(response.data.decode("UTF-8"))
        else:
            logger.warning(f"Invalid response received from sensor {self.name}")
            return 0