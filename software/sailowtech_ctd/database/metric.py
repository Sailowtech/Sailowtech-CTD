from .base import db

class Metric(db.Entity):
    name: str
    unit: str

