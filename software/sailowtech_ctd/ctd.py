import csv
import datetime
import time
from enum import Enum, auto

import smbus2 as smbus

from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.run import Run
from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.database.sensor import assert_sensor

from software.sailowtech_ctd.logger import logger

class TooShortInterval(Exception):
    pass


class CTD:
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    def __init__(self, bus=DEFAULT_BUS):
        self.name: str = ''
        self._sensors: list[GenericSensor] = []
        self.min_delay: float = 1.05
        self._last_measurement: float = 0.
        self._data = []
        self._activated: bool = False

        try:
            self._bus = smbus.SMBus(bus)
        except:
            print("Bus %d is not available." % bus)
            print("Available busses are listed as /dev/i2c*")
            self._bus = None

    @property
    def is_bus_connected(self) -> bool:
        """Indicates if the object has a I2C-Bus connected"""
        return self._bus is not None

    @property
    def sensors(self):
        """Return the list of all the sensors that have been configured"""
        return self._sensors

    def set_sensors(self, val):
        """Set a new list of configured sensors"""
        self._sensors = val

    @property
    def atlas_sensors(self):
        return [sensor for sensor in self._sensors if sensor.brand == SensorBrand.Atlas]

    @property
    def bluerobotics_sensors(self):
        return [sensor for sensor in self._sensors if sensor.brand == SensorBrand.BlueRobotics]

    @property
    def activated(self):
        return self._activated


    def setup_sensors(self):
        if len(self.sensors) == 0: logger.error("Initialize sensors before setup!"); exit(1)
        self.min_delay = max([sensor.min_delay for sensor in self.sensors])
        logger.info(f"Minimum delay was initialised to {self.min_delay} seconds")
        for sensor in self.sensors:
            sensor.init(self._bus)
            assert_sensor(sensor)

        self._activated = True


    def measure_all(self, run_id: int):
        for sensor in self.sensors:
            sensor.write_read_command(self._bus)
        time.sleep(self.min_delay)
        timestamp = datetime.datetime.now()
        for sensor in self.sensors:
            measured_value = sensor.read_result(self._bus)
            sensor_obj = assert_sensor(sensor)
            Measurement.create(sensor = sensor_obj.get_id(), value = measured_value, run = Run.get(id = run_id).id, timestamp=timestamp)
