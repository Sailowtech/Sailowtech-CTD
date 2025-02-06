import yaml
from software.sailowtech_ctd import logger
from software.sailowtech_ctd.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.sensors.bluerobotics import DepthSensor
from software.sailowtech_ctd.sensors.generic import GenericSensor
import os
import pathlib

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
            case _:
                logger.warning(f"Sensor {n} was not set up. Wrong name?")

    return sensors