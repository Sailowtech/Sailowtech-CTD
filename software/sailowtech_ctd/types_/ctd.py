from dataclasses import dataclass
from enum import Enum, auto
from typing import Union

import yaml

from software.sailowtech_ctd.types_.sensors.generic import GenericSensor
from software.sailowtech_ctd.types_.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.types_.sensors.blue_robotics import BlueRoboticsSensor


class SensorBrand(Enum):
    Atlas = auto()
    BlueRobotics = auto()


class SensorType(Enum):
    # Atlas
    DISSOLVED_OXY = auto()
    CONDUCTIVITY = auto()
    DISSOLVED_OXY_TEMP = auto()
    # Blue robotics
    DEPTH = auto()


@dataclass
class Sensor:
    type: SensorType
    name: str
    address: int
    brand: SensorBrand


class CTD:
    # I'm sorry for this. Hardcoding all the sensors.
    DEFAULT_SENSORS: list[Sensor] = [
        Sensor(SensorType.DISSOLVED_OXY, "Dissolved Oxygen", 0x61, SensorBrand.Atlas),
        Sensor(SensorType.CONDUCTIVITY, "Conductivity Probe", 0x64, SensorBrand.Atlas),
        Sensor(SensorType.DISSOLVED_OXY_TEMP, "Temperature from Dissolved Oxygen Sensor", 0x66, SensorBrand.Atlas),
        Sensor(SensorType.DEPTH, "Depth Sensor", 0x76, SensorBrand.BlueRobotics),
    ]

    MEASUREMENTS_INTERVAL = 1  # seconds

    def __init__(self, config_path):
        self.name: str = ''
        # self.sensors_config: dict[str, dict[str, dict[str, str]]] = {}
        self._sensors: list[
            Union[GenericSensor, Sensor]] = []  # For now, accepts generic and Sensor dataclass. Choose one later
        self.interval: float = 0.

        # self.load_config(config_path)

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

    # todo : check time interval is greater than sum of time limit for each sensor

    def measure(self, sensor: Sensor):
        pass

    def start_measurements(self):
        for sensor in self.sensors:
            print(f'Measuring {sensor.name} ...')
