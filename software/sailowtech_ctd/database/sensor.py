from pony.orm import Set

from .base import db
from .metric import Metric
from ..sensors.types import SensorTypes

class Sensor(db.Entity):
    name: str
    metrics: Set(Metric)
    device: SensorTypes