#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program aims to facilitate communication with multiple sensors inside a CTD.
For now, it supports I2C protocol but there should be more in the future.

Credits for I2C protocol: "https://github.com/Atlas-Scientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py"]
Contact                 : "arthur.jacobs@sailowtech.ch"
"""
from datetime import datetime
import time
from pprint import pprint

from pony.orm import commit, db_session

from database import db
from database.metric import Metric
from database.sensor import Sensor
from database.measurement import Measurement
from ctd import CTD
from sensors.types import Sensor as SensorType

db_params = {'provider': 'sqlite', 'filename': 'debug.sqlite', 'create_db': True}

if __name__ == '__main__':
    ctd = CTD()
    db.bind(**db_params)
    db.generate_mapping(create_tables=True)
    with db_session:
        m1 = Metric(name="temperature", unit="Celsius")
        s1 = Sensor(name="test-sensor", device=SensorType.ATLAS_EZO_DO)

    #ctd.setup_sensors()

    pprint(ctd.sensors)

    # input("Appuyez sur Entrée pour procéder à la calibration des capteurs...\n")
    # ctd.calibrate_sensors()

    ctd.pressure_threshold = int(input("Threshold de coupure des mesures (mba)(généralement 200 à 500 mbars) : "))
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
    ctd.export_csv(f'{str_now}_data.csv')
    print("Exported csv, exiting program")
