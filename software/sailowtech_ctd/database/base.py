from peewee import *
db = SqliteDatabase('data/debug.sqlite')

class BaseModel(Model):
    class Meta:
        database = db