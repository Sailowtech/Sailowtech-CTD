from datetime import datetime

from pony.orm import Required, Optional

from .base import db
from .metric import Metric
from .run import Run
from .sensor import Sensor


class Measurement(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    run = Required("Run")
    sensor = Required("Sensor")
    metric = Optional("Metric")
    value = Required(float)