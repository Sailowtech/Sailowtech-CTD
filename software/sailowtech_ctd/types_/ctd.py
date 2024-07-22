import yaml

from software.sailowtech_ctd.types_.sensors.generic import GenericSensor
from software.sailowtech_ctd.types_.sensors.atlas import AtlasSensor
from software.sailowtech_ctd.types_.sensors.blue_robotics import BlueRoboticsSensor


class CTD:
    def __init__(self, config_path):
        self.name: str = ''
        self.sensors_config: dict[str, dict[str, dict[str, str]]] = {}
        self.sensors: list[GenericSensor] = []
        self.interval: float = 0.

        self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.name = config["device"]
        self.sensors_config = config["sensors"]
        self.interval = config["measurements-interval"]

    def setup_sensors(self):
        for atlas_sensors in self.sensors_config["atlas-sensors"].keys():
            self.sensors.append(AtlasSensor(**self.sensors_config["atlas-sensors"][atlas_sensors]))

        for blue_robotics_sensors in self.sensors_config["bluerobotics-sensors"].keys():
            self.sensors.append(
                BlueRoboticsSensor(**self.sensors_config["bluerobotics-sensors"][blue_robotics_sensors]))

    def start(self):
        pass
