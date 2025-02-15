from datetime import datetime

from peewee import *
from .base import BaseModel
from .run import Run
from .sensor import Sensor


class Measurement(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    run = ForeignKeyField(Run, backref="measurements")
    sensor = ForeignKeyField(Sensor, backref="measurements")
    value = FloatField()