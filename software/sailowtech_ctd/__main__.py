#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program aims to facilitate communication with multiple sensors inside a CTD.
For now, it supports I2C protocol but there should be more in the future.

Credits for I2C protocol: "https://github.com/Atlas-Scientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py"
Contact                 : "arthur.jacobs@sailowtech.ch"
"""

from datetime import datetime
import time

import uvicorn
import threading

from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.metric import Metric, assert_metrics_setup
from software.sailowtech_ctd.database.sensor import Sensor
from software.sailowtech_ctd.logger import logger
from software.sailowtech_ctd.database import db
from software.sailowtech_ctd.ctd import CTD
from software.sailowtech_ctd.database.run import Run, RunTypes

from software.sailowtech_ctd.methods.config_parser import load_file_to_yaml, get_sensors, is_mock


def start():
    """Start app with uvicorn"""
    web_thread = threading.Thread(target=uvicorn.run, kwargs={"app": "software.sailowtech_ctd.webapi.app:app", "host": "0.0.0.0", "port": 80})
    logger.info("Starting web service thread...")
    web_thread.start()
    logger.info("Started web service thread")
    main_loop("software/sailowtech_ctd/config.yaml")


def start_debug():
    """Start app with uvicorn"""
    web_thread = threading.Thread(target=uvicorn.run, kwargs={"app": "software.sailowtech_ctd.webapi.app:app", "host": "0.0.0.0", "port": 8000})
    logger.info("Starting web service thread...")
    web_thread.start()
    logger.info("Started web service thread")
    main_loop("software/sailowtech_ctd/config-mock.yaml")


def init_db():
    db.connect()
    db.create_tables([Measurement, Run, Sensor, Metric])
    assert_metrics_setup()

def main_loop(configfile: str):
    logger.info("Main Loop is starting")
    sel = Run.select().where(Run.running == True)
    if len(sel) > 0:
        logger.info("Stopping all currently running Runs")
        for r in sel:
            r.running = False
            r.save()

    config = load_file_to_yaml(configfile)
    mockery = is_mock(config)

    ctd = CTD()
    ctd.set_sensors(get_sensors(config))
    ctd.setup_sensors()

    while True:
        logger.info("Checking for active runs")
        sel = Run.select().where(Run.running == True)
        if len(sel) > 1: logger.warning("More than one run is started!")
        if len(sel) > 0:
            logger.info(f"Found {len(sel)} active runs")
            for r in sel[:]:
                match r.run_type:
                    case RunTypes.MANUAL_STOP:
                        pass
                    case RunTypes.TIME_DURATION:
                        if (datetime.now() - r.timestamp).total_seconds() >= r.wanted_duration:
                            r.running = False
                            r.save()
                            logger.info(f"Stopped run with id {r.id} since time run out")
                    case RunTypes.MEASUREMENT_COUNT:
                        if r.measurements.count() >= r.wanted_measurements:
                            r.running = False
                            r.save()
                        logger.info(f"Stopped run with id {r.id} since measurement limit was reached")
                logger.info(f"Checking if measuring is necessary for run {r.id}")
                if ctd.is_bus_connected | mockery:
                    logger.info(f"Measuring for run {r.id}")
                    ctd.measure_all(r.id)
                else:
                    logger.error("CTD Bus is not connected")
        else:
            time.sleep(1) # Info: we are only sleeping when nothing is running to improve efficiency


if __name__ == '__main__':
    start_debug()
