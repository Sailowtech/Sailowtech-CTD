from pony.orm import Required, Set

from .base import db

class Metric(db.Entity):
    name = Required(str)
    unit = Required(str)
    measurements = Set("Measurement")

