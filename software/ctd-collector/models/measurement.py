from pony.orm import *
from .base import db
import datetime

class Measurement(db.Entity):
    sensor = Required(str)
    reading = Required(float)
    timestamp = Required(datetime.datetime, default=datetime.datetime.now())
