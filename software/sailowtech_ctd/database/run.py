from pony.orm import Required, Set
from datetime import datetime
from .base import db

class Run(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    measurements = Set("Measurement")

