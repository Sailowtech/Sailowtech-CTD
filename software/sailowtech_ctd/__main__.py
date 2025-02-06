#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program aims to facilitate communication with multiple sensors inside a CTD.
For now, it supports I2C protocol but there should be more in the future.

Credits for I2C protocol: "https://github.com/Atlas-Scientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py"]
Contact                 : "arthur.jacobs@sailowtech.ch"
"""
import logging
from datetime import datetime
import time
import sys
from pony.orm import db_session

from software.sailowtech_ctd.database import db
from software.sailowtech_ctd.database.metric import Metric
from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.sensor import Sensor
from software.sailowtech_ctd.ctd import CTD
from software.sailowtech_ctd.sensors.types import Sensor as SensorType

from software.sailowtech_ctd.methods.config_parser import load_file_to_yaml, get_sensors

db_params = {'provider': 'sqlite', 'filename': '../../data/debug.sqlite', 'create_db': True}

def script_entry():
    if len(sys.argv) < 2:
        logging.info("No path provided as script argument. Using the default software/sailowtech_ctd/config.yaml")
        configfile = "software/sailowtech_ctd/config.yaml"
    else:
        configfile = sys.argv[1]
    main(configfile)

def main(configfile: str):
    config = load_file_to_yaml(configfile)

    ctd = CTD()
    ctd.set_sensors(get_sensors(config))
    db.bind(**db_params)
    db.generate_mapping(create_tables=True)
    with db_session:
        m1 = Metric(name="temperature", unit="Celsius")
        s1 = Sensor(name="test-sensor", device=SensorType.ATLAS_EZO_DO)

    # ctd.setup_sensors()

    # input("Appuyez sur Entrée pour procéder à la calibration des capteurs...\n")
    # ctd.calibrate_sensors()

    ctd.pressure_threshold = int(input("CTD pressure cut-off in mBar (generally 200 to 500 mBar): "))
    if ctd.is_bus_connected:
        ctd.measure_all()
    else:
        print("i2C Bus not connected!")
    i = 0
    while i < 30 and ctd.activated and ctd.is_bus_connected:
        ctd.measure_all()
        time.sleep(1)
        i += 1

    str_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ctd.export_csv(f'data/{str_now}_data.csv')
    print("Exported csv, exiting program")

if __name__ == '__main__':
    main("config.yaml")
