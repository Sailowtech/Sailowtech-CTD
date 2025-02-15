import smbus2 as smbus
import random

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.sensors.types import Sensor

class MockSensor(GenericSensor):
    """
    Class which provides a mock sensor in order to be able to test the interface
    """
    def __init__(self, brand: SensorBrand, sensor_type: Sensor, name: str, address: int, min_val: int, max_val: int, min_delay: float = 1):
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
        self.min_delay = min_delay
        super().__init__(brand, sensor_type, name, address, self.min_delay)

    def init(self, bus: smbus.SMBus):
        """
        Initialises the mock sensor. Always returns true since no setup is required
        :param bus: The bus to be used - is ignored
        :return: Returns True
        """
        return True

    def write_read_command(self, bus: smbus.SMBus) -> bool:
        """
        Method to write the read command to the sensor - is ignored
        :param bus: The bus to be used - is ignored
        :return: Returns True
        """
        return True

    def read_result(self, bus: smbus.SMBus) -> float:
        """
        Method to read the measurement result
        :param bus: The bus to be used - is ignored
        :return: Returns the measured value
        """
        return self.measure_value(bus)

    def measure_value(self, bus: smbus.SMBus):
        """
        Measure the value of the mock sensor. Returns a random value between the minimum and maximum set during class instantiation
        :param bus: The bus to be used - is ignored
        :return: Returns the randomly generated simulated measurement
        """
        return random.uniform(self.min, self.max)