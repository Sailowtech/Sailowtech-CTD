import csv
import datetime
import time

import smbus2 as smbus

from software.sailowtech_ctd.common import DataFields, OutputTypes
from software.sailowtech_ctd.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.sensors.bluerobotics import DepthSensor
from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand

from sensors.types import Sensor

from logger import logger

class TooShortInterval(Exception):
    pass


class CTD:
    # I'm sorry for this. Hardcoding all the sensors.
    DEFAULT_SENSORS: list[GenericSensor] = [
        DepthSensor("Depth Sensor", 0x76, min_delay=0.3),
        AtlasSensor(Sensor.ATLAS_EZO_DO, "Dissolved Oxygen", 0x61),
        AtlasSensor(Sensor.ATLAS_EZO_CONDUCTIVITY, "Conductivity Probe", 0x64),
        AtlasSensor(Sensor.ATLAS_EZO_TEMP, "Temperature from Dissolved Oxygen Sensor", 0x66),
    ]

    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    MEASUREMENTS_INTERVAL = 1  # seconds

    DEFAULT_THRESHOLD = 500  # By default, : 500mba (~5m of water)

    def __init__(self, bus=DEFAULT_BUS, output: OutputTypes=OutputTypes.SQL, useConfig: bool = True):

        self.output: OutputTypes = OutputTypes.SQL
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
        print(f"Threshold set to : {self._pressure_threshold} mba")

    def setup_sensors(self):
        if len(self.sensors) == 0: logger.error("Initialize sensors before setup!"); exit(1)

        # Compute global minimum delay
        self._min_delay = sum([sensor.min_delay for sensor in self.sensors])

        for sensor in self.sensors:
            sensor.init(self._bus)

        self._activated = True


    def measure_all(self):

        print(self.output)


        if time.time() - self._last_measurement < self.MEASUREMENTS_INTERVAL:
            print("Wait longer !")
            raise TooShortInterval()

        depth_sensor_output = self.DEFAULT_SENSORS[0].measure_value(self._bus)

        for i in range(3):  # Test Read Atlas
            print(self.DEFAULT_SENSORS[i + 1].measure_value(self._bus))

        # Check for end of measurements (we stop when we go up enough)
        if self._max_pressure - depth_sensor_output[DataFields.PRESSURE_MBA] >= self._pressure_threshold:
            self._activated = False
            print("Stopped because went up")
        else:
            self._max_pressure = max(self._max_pressure, depth_sensor_output[DataFields.PRESSURE_MBA])

        now = datetime.datetime.now()

        time_values = {DataFields.TIMESTAMP: now.timestamp(),
                       DataFields.DATE: now.strftime("%Y-%m-%d %H:%M:%S")}

        self._data.append(time_values | depth_sensor_output)
        print(f'Depth value: {depth_sensor_output[DataFields.DEPTH_METERS]}\n'
              f'Pressure (mba) : {depth_sensor_output[DataFields.PRESSURE_MBA]}\n'
              f'Temperature (C) : {depth_sensor_output[DataFields.TEMPERATURE]}\n')

    def export_csv(self, path: str):
        fields = [DataFields.TIMESTAMP, DataFields.DATE,
                  DataFields.PRESSURE_MBA, DataFields.DEPTH_METERS,
                  DataFields.TEMPERATURE]

        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)

            # Write the field names
            csvwriter.writeheader()

            # Write the data
            csvwriter.writerows(self._data)
