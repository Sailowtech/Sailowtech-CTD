from datetime import datetime

from pony.orm import Required, Optional

from .base import db
from .run import Run
from .sensor import Sensor


class Measurement(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    run = Required("Run")
    sensor = Required("Sensor")
    value = Required(float)