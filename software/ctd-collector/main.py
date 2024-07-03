import yaml
from atlas_i2c import commands, sensors, atlas_i2c

sensor_objects = []

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

if "atlas-sensors" in cfg:
    for sensor_cfg in cfg["atlas-sensors"]:
        sensor = sensors.Sensor(sensor_cfg["name"], sensor_cfg["address"])
        sensor_objects.append(sensor)