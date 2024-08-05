#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program aims to facilitate communication with multiple sensors inside a CTD.
For now, it supports I2C protocol but there should be more in the future.

Credits for I2C protocol: "https://github.com/Atlas-Scientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py"]
Contact                 : "arthur.jacobs@sailowtech.ch"
"""
import time
from pprint import pprint

from types_.ctd import CTD

if __name__ == '__main__':
    ctd = CTD(config_path="config.yaml")
    ctd.setup_sensors()

    pprint(ctd.sensors)

    # input("Appuyez sur Entrée pour procéder à la calibration des capteurs...\n")
    # ctd.calibrate_sensors()

    i = 0
    while i < 1000 and ctd.activated:
        ctd.measure_all()
        time.sleep(1)
        i += 1

    ctd.export_csv('data.csv')
