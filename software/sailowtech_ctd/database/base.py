import os
import pathlib

from peewee import *
db = SqliteDatabase(os.path.abspath(os.path.join(pathlib.Path(os.path.dirname(__file__)).parent.parent.parent, 'data/debug.sqlite')))

class BaseModel(Model):
    class Meta:
        database = db