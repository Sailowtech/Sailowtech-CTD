from peewee import *
from .base import BaseModel
from software.sailowtech_ctd.sensors.types import SensorTypeField
from software.sailowtech_ctd.sensors.types import Metric as MetricType
from ..sensors.generic import GenericSensor
from .metric import Metric

class Sensor(BaseModel):
    """
    Sensor Model for the database
    """
    name = TextField(unique=True)
    device = SensorTypeField()
    metric = ForeignKeyField(Metric, backref="sensors")


def assert_sensor(sensor: GenericSensor) -> Sensor:
    """
    Helper method to assert that a specified sensor exists in the database. Creates it if it doesn't exist.
    :param sensor: The sensor which should be created
    :return: Returns the database object of the sensor
    """
    return Sensor.get_or_create(name=sensor.name, device=sensor.sensor_type, metric=Metric.get(type=sensor.metric_type))[0]