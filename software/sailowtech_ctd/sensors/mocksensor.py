import smbus2 as smbus
import random

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.sensors.types import Sensor

class MockSensor(GenericSensor):
    """
    Class which provides a mock sensor in order to be able to test the interface
    """
    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min_val: int, max_val: int):
        """
        Initialise the mock sensor
        :param brand: Brand of the sensor (mock_sensor)
        :param sensor_type: Type of the sensor (mock_sensor)
        :param name: The given name for this sensor
        :param address: The address assigned to this sensor (is ignored)
        :param min_val: The minimum value that the mock sensor is returning
        :param max_val: The maximum value that the mock sensor is returning
        """
        self.min = min_val
        self.max = max_val
        super().__init__(brand, sensor_type, name, address)

    def init(self, bus: smbus.SMBus):
        """
        Initialises the mock sensor. Always returns true since no setup is required
        :param bus: The bus to be used - is ignored
        :return: Returns True
        """
        return True

    def measure_value(self, bus: smbus.SMBus):
        """
        Measure the value of the mock sensor. Returns a random value between the minimum and maximum set during class instantiation
        :param bus: The bus to be used - is ignored
        :return: Returns the randomly generated simulated measurement
        """
        return random.uniform(self.min, self.max)