from pony.orm import Set, Required, PrimaryKey, db_session

from .base import db
from software.sailowtech_ctd.sensors.types import Sensor as SensorType
from ..sensors.generic import GenericSensor


class Sensor(db.Entity):
    name = Required(str)
    device = Required(SensorType)
    measurements = Set("Measurement")


def assert_sensor(sensor: GenericSensor) -> Sensor:
    with db_session:
        if not Sensor.exists(name=sensor.name, device=sensor.sensor_type):
            return Sensor(name=sensor.name, device=sensor.sensor_type)
        else:
            return Sensor.get(name=sensor.name, device=sensor.sensor_type)