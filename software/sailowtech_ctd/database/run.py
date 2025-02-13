from enum import Enum

from pony.orm import Required, Set, Optional, db_session
from datetime import datetime
from .base import db
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


class Run(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    measurements = Set("Measurement")
    run_type = Required(RunTypes)
    wanted_duration = Optional(int)
    wanted_measurements = Optional(int)
    running = Required(bool, default=True)

def stop_run(run_id: int) -> bool:
    with db_session:
        res = Run.get(id=run_id)
        if res is None:
            return False
        else:
            res.running = False
            return True


def create_run(run_type: RunTypes, run_data: None | int) -> int:
    with db_session:
        match run_type:
            case RunTypes.MANUAL_STOP:
                r = Run(run_type=run_type)
            case RunTypes.TIME_DURATION:
                if run_data is None: logger.error("run_data not specified!!"); run_data = 0;
                r = Run(run_type=run_type, wanted_duration=run_data)
            case RunTypes.MEASUREMENT_COUNT:
                if run_data is None: logger.error("run_data not specified!!"); run_data = 0;
                r = Run(run_type=run_type, wanted_measurements=run_data)
        r.flush()
        logger.info(f"Created run with ID {r.id}, type {run_type} and parameter {run_data}")
        return r.id