from enum import Enum, auto

from software.sailowtech_ctd.types_.sensors.generic import GenericSensor, SensorType, SensorBrand


class BlueRoboticsSensor(GenericSensor):
    class Commands(Enum):
        READ = auto()

    def __init__(self, sensor_type: SensorType, name: str, address: int, min_delay: float = 1):
        super().__init__(SensorBrand.Atlas, sensor_type, name, address, min_delay)