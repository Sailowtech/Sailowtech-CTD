from enum import Enum, auto

from generic import GenericSensor, SensorBrand, SensorType


class AtlasSensor(GenericSensor):
    class Commands(Enum):
        READ = auto()

    def __init__(self, sensor_type: SensorType, name: str, address: int, min_delay: float = 1):
        super().__init__(SensorBrand.Atlas, sensor_type, name, address, min_delay)
