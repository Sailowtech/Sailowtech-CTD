import yaml
from software.sailowtech_ctd import logger
from software.sailowtech_ctd.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.sensors.bluerobotics import DepthSensor
from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
import os
import pathlib

from software.sailowtech_ctd.sensors.mocksensor import MockSensor
from software.sailowtech_ctd.sensors.types import Sensor


def load_file_to_yaml(path: str) -> object:
    """
    Tries to load the config file at the specified path
    :param path: The path to the config file
    :return: Returns a python object of the yaml file to be further used
    """
    try:
        path = os.path.join(pathlib.Path(os.getcwd()), path)
        config = open(path)
    except FileNotFoundError:
        logger.error(f"Config file not found at {path}")
        exit(1)
    else:
        with config:
            return yaml.safe_load(config)

def is_mock(config: object) -> bool:
    """
    Check if the config file has the mock attribute, which means the software is running in a test environment
    :param config: The config object
    :return: Returns a boolean to check if it is a mock config
    """
    if "mock" in config:
        return config["mock"]
    else:
        return False

def get_interval(config: object) -> int:
    """
    Get the measurement interval specified in the config
    :param config: The config object
    :return: Returns an int of the measurement interval in seconds
    """
    if "interval" not in config:
        logger.error("No interval configured in Config!"); exit(1)
    else:
        return config["interval"]

def get_threshold(config: object) -> int:
    """
    Get the depth cutoff threshold specified in the config
    :param config: The config object
    :return: Returns an int of the depth threshold
    """
    if "threshold" not in config:
        logger.error("No threshold configured in Config!"); exit(1)
    else:
        return config["threshold"]

def get_sensors(config: object) -> list[GenericSensor]:
    """
    Get the list of Sensor objects from the previously loaded config
    :param config: The config object
    :return: Returns a list of Sensors (GenericSensor)
    """
    if "sensors" not in config: logger.error("No sensors configured in Config!"); exit(1)
    sensors = []
    for sensor in config["sensors"]:
        n = sensor
        sensor = config["sensors"][sensor]
        if "sensor-type" not in sensor: logger.error(f"Attribute sensor-type not defined for sensor {n}"); exit(1)
        if "name" not in sensor: logger.error(f"Attribute name not defined for sensor {n}"); exit(1)
        if "address" not in sensor: logger.error(f"Attribute address not defined for sensor {n}"); exit(1)
        match sensor["sensor-type"]:
            case "ATLAS_EZO_DO":
                s = AtlasSensor(Sensor.ATLAS_EZO_DO, sensor["name"], sensor["address"])
                sensors.append(s)
            case "ATLAS_EZO_CONDUCTIVITY":
                s = AtlasSensor(Sensor.ATLAS_EZO_CONDUCTIVITY, sensor["name"], sensor["address"])
                sensors.append(s)
            case "ATLAS_EZO_TEMP":
                s = AtlasSensor(Sensor.ATLAS_EZO_TEMP, sensor["name"], sensor["address"])
                sensors.append(s)
            case "BLUEROBOTICS_BAR30_DEPTH":
                min_delay = 1
                if "min-delay" in sensor: min_delay = sensor["min-delay"]
                s = DepthSensor(sensor["name"], sensor["address"], min_delay)
                sensors.append(s)
            case "MOCK_SENSOR":
                s = MockSensor(SensorBrand.MockBrand, Sensor.MOCK_SENSOR, sensor["name"], sensor["address"], sensor["min"], sensor["max"])
                sensors.append(s)
            case _:
                logger.warning(f"Sensor {n} was not set up. Wrong name?")

    return sensors