import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union

import yaml

from software.sailowtech_ctd.types_.sensors.generic import GenericSensor, SensorType
from software.sailowtech_ctd.types_.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.types_.sensors.bluerobotics import BlueRoboticsSensor


class TooShortInterval(Exception):
    pass


class CTD:
    # I'm sorry for this. Hardcoding all the sensors.
    DEFAULT_SENSORS: list[GenericSensor] = [
        AtlasSensor(SensorType.DISSOLVED_OXY, "Dissolved Oxygen", 0x61),
        AtlasSensor(SensorType.CONDUCTIVITY, "Conductivity Probe", 0x64),
        AtlasSensor(SensorType.DISSOLVED_OXY_TEMP, "Temperature from Dissolved Oxygen Sensor", 0x66),
        BlueRoboticsSensor(SensorType.DEPTH, "Depth Sensor", 0x76),
    ]

    MEASUREMENTS_INTERVAL = 1  # seconds

    def __init__(self, config_path):
        self.name: str = ''
        # self.sensors_config: dict[str, dict[str, dict[str, str]]] = {}
        self._sensors: list[GenericSensor] = []

        # self.load_config(config_path)

        self._min_delay: float = 3.
        self._last_measurement: float = 0.

    @property
    def sensors(self):
        return self._sensors

    @sensors.setter
    def sensors(self, val):
        self._sensors = val

    @property
    def atlas_sensors(self):
        return [sensor for sensor in self._sensors if sensor.brand == SensorBrand.Atlas]

    @property
    def bluerobotics_sensors(self):
        return [sensor for sensor in self._sensors if sensor.brand == SensorBrand.BlueRobotics]

    # TODO : hardcoded for now
    # def load_config(self, config_path):
    #     with open(config_path) as f:
    #         config = yaml.load(f, Loader=yaml.FullLoader)
    #
    #     self.name = config["device"]
    #     self.sensors_config = config["sensors"]
    #     self.interval = config["measurements-interval"]

    # def setup_sensors(self):
    #     for atlas_sensors in self.sensors_config["atlas-sensors"].keys():
    #         self.sensors.append(AtlasSensor(**self.sensors_config["atlas-sensors"][atlas_sensors]))
    #
    #     for blue_robotics_sensors in self.sensors_config["bluerobotics-sensors"].keys():
    #         self.sensors.append(
    #             BlueRoboticsSensor(**self.sensors_config["bluerobotics-sensors"][blue_robotics_sensors]))

    def setup_sensors(self):
        self.sensors = self.DEFAULT_SENSORS

        # Compute global minimum delay
        self._min_delay = sum([sensor.min_delay for sensor in self.sensors])

        # self._calibrate_atlas_sensors()
        # self._calibrate_bluerobotics_sensors()

    def measure(self, sensor: Sensor):
        """

        :param sensor:
        :return: None if error / not supported, float value instead
        """

        if time.time() - sensor.last_read < sensor.min_delay:
            print(f"Sensor '{sensor.name}' needs to wait longer between measurements !")
            raise TooShortInterval()

        measurement: float = None
        if sensor.brand == SensorBrand.BlueRobotics:
            # Do something
            pass
        elif sensor.brand == SensorBrand.Atlas:
            # Do something
            pass
        else:
            print(f"Sensor brand '{sensor.brand}' not supported yet !")

        return measurement

    def measure_all(self):
        if time.time() - self._last_measurement < self.MEASUREMENTS_INTERVAL:
            print("Wait longer !")
            raise TooShortInterval()

        results = dict()
        for sensor in self.sensors:
            results[sensor.type] = self.measure(sensor)
