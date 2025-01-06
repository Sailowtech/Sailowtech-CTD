from datetime import datetime

from pony.orm import Required

from .base import db
from .metric import Metric
from .sensor import Sensor


class Measurement(db.Entity):
    timestamp: datetime = datetime.now()
    sensor = Required("Sensor")
    metric = Required("Metric")
    value = Required(float)