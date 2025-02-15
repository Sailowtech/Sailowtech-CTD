from enum import Enum

from peewee import *
from datetime import datetime
from .base import db, BaseModel
from ..logger import logger

class RunTypes(int, Enum):
    """
    The types of runs that we can create.
    - Manual stop: Measure until stopped manually
    - Time duration: Measure until time has passed (seconds)
    - Measurement count: Measure until we have measured a specified amount of times
    """

    MANUAL_STOP: int = 0
    TIME_DURATION: int = 1
    MEASUREMENT_COUNT: int = 2

class RunTypeField(Field):
    field_type = 'runtype'

    def db_value(self, value):
        return value.value

    def python_value(self, value):
        return RunTypes(value)

class Run(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    run_type = RunTypeField()
    wanted_duration = IntegerField(default=None, null=True)
    wanted_measurements = IntegerField(default=None, null=True)
    running = BooleanField(default=True)

def stop_run(run_id: int) -> bool:
    """
    Stop the run specified
    :param run_id: The id of the run to be stopped
    :return: Return true if the run was found and stopped, false otherwise
    """
    res = Run.get(Run.id == run_id)
    if res is None:
        return False
    else:
        res.running = False
        res.save()
        return True


def create_run(run_type: RunTypes, run_data: None | int) -> int:
    """
    Create a run
    :param run_type: The type of the run to be created, according to the `RunTypes` enum
    :param run_data: The data required for the run_type. Not required for all the RunTypes
    :return: Return the id of the newly created run
    """
    match run_type:
        case RunTypes.MANUAL_STOP:
            r = Run.create(run_type=run_type)
        case RunTypes.TIME_DURATION:
            if run_data is None: logger.error("run_data not specified!!"); run_data = 0;
            r = Run.create(run_type=run_type, wanted_duration=run_data)
        case RunTypes.MEASUREMENT_COUNT:
            if run_data is None: logger.error("run_data not specified!!"); run_data = 0;
            r = Run.create(run_type=run_type, wanted_measurements=run_data)
        case _:
            r = None
            logger.error(f"Run with type {run_type} was not created. Missing implementation!")

    r.save()
    logger.info(f"Created run with ID {r.id}, type {run_type} and parameter {run_data}")
    return r.id