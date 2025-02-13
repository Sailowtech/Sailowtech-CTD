import csv
import time
from enum import Enum, auto

import smbus2 as smbus

from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.run import Run
from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from software.sailowtech_ctd.database.sensor import assert_sensor

from pony.orm import db_session

from software.sailowtech_ctd.logger import logger

class TooShortInterval(Exception):
    pass


class CTD:
    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    MEASUREMENTS_INTERVAL = 1  # seconds

    DEFAULT_THRESHOLD = 500  # By default, : 500mba (~5m of water)

    def __init__(self, bus=DEFAULT_BUS):
        self.name: str = ''
        self._sensors: list[GenericSensor] = []

        # self.load_config(config_path)

        self._min_delay: float = 3.
        self._last_measurement: float = 0.

        self._data = []

        self._activated: bool = False
        self._max_pressure: float = 0.  # To stop program when lifting the CTD up
        self._pressure_threshold: int = self.DEFAULT_THRESHOLD

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

    @property
    def pressure_threshold(self):
        return self._pressure_threshold

    @pressure_threshold.setter
    def pressure_threshold(self, val):
        self._pressure_threshold = (val if val else self.DEFAULT_THRESHOLD)
        print(f"Threshold set to: {self._pressure_threshold} mba")

    def setup_sensors(self):
        if len(self.sensors) == 0: logger.error("Initialize sensors before setup!"); exit(1)

        # Compute global minimum delay
        self._min_delay = sum([sensor.min_delay for sensor in self.sensors])

        for sensor in self.sensors:
            sensor.init(self._bus)
            assert_sensor(sensor)

        self._activated = True


    def measure_all(self, run_id: int):
        if time.time() - self._last_measurement < self.MEASUREMENTS_INTERVAL:
            print("Wait longer!")
            raise TooShortInterval()

        for sensor in self.sensors:
            sensor.write_read_command(self._bus)
        time.sleep(1.05)
        for sensor in self.sensors:
            measured_value = sensor.read_result(self._bus)
            with db_session:
                sensor_obj = assert_sensor(sensor)
                Measurement(sensor = sensor_obj, value = measured_value, run = Run.get(id = run_id))
