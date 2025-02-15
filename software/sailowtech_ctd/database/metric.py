from peewee import *
from .base import BaseModel
from ..logger import logger
from ..sensors.types import MetricTypeField
from ..sensors.types import Metric as MetricEnum


class Metric(BaseModel):
    name = TextField()
    unit = TextField()
    type = MetricTypeField(unique=True)


def assert_metrics_setup() -> None:
    """
    Make sure that all the metrics are set up with the default units.
    :return: Returns nothing (None)
    """
    if Metric.get_or_create(name="Depth", unit="m", type=MetricEnum.DEPTH)[1]: logger.info("Added Depth metric to DB")
    if Metric.get_or_create(name="Pressure", unit="mBar", type=MetricEnum.PRESSURE)[1]: logger.info("Added Pressure metric to DB")
    if Metric.get_or_create(name="Temperature", unit="°C", type=MetricEnum.TEMPERATURE)[1]: logger.info("Added Temperature metric to DB")
    if Metric.get_or_create(name="Dissolved Oxygen", unit="mg/L", type=MetricEnum.DISSOLVED_OXYGEN)[1]: logger.info("Added Dissolved Oxygen metric to DB")
    if Metric.get_or_create(name="Conductivity", unit="μS/cm", type=MetricEnum.CONDUCTIVITY)[1]: logger.info("Added Conductivity metric to DB")