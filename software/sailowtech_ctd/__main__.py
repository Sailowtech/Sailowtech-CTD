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

    i = 0
    while True and i < 1000:
        ctd.measure_all()
        time.sleep(1)
        i += 1
