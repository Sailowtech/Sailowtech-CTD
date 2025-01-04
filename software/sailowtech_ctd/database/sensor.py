from pony.orm import Set, Required

from .base import db
from software.sailowtech_ctd.sensors.types import Sensor

class Sensor(db.Entity):
    name = Required(str)
    device = Required(Sensor)
    measurements = Set("Measurement")