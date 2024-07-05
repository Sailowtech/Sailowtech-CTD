import yaml
from atlas_i2c import commands, sensors, atlas_i2c
from pony.orm import *
from models import db
from models import Measurement

db.bind(provider='sqlite', filename='measurements.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def write_reading(sensor, reading):
    Measurement(sensor=sensor, reading=float(reading))

atlas_sensors = []
bluerobotics_sensors = []

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

if "atlas-sensors" in cfg:
    for sensor_cfg in cfg["atlas-sensors"]:
        sensor = sensors.Sensor(cfg["atlas-sensors"][sensor_cfg]["name"], cfg["atlas-sensors"][sensor_cfg]["address"])
        atlas_sensors.append(sensor)

if "bluerobotics-sensors" in cfg:
    for sensor_cfg in cfg["bluerobotics-sensors"]:
        #sensor = sensors.Sensor(cfg["bluerobotics-sensors"][sensor_cfg]["name"], cfg["bluerobotics-sensors"][sensor_cfg]["address"])
        import ms5837
        # https://github.com/bluerobotics/ms5837-python
        sensor = ms5837.MS5837() # Use defaults (MS5837-30BA device on I2C bus 1)
        bluerobotics_sensors.append(sensor)




while True:
    for sensor in atlas_sensors:
        sensor.connect()
        response = sensor.query(commands.READ)
        write_reading(sensor.name, response.data.decode("UTF-8"))
        print(f"Data for {sensor.name}: {response.data}")

    for sensor in bluerobotics_sensors:
        sensor.init()
        sensor.read(ms5837.OSR_256)
        write_reading("Bluerobotics Pressure", sensor.pressure())
        write_reading("Bluerobotics Temperature", sensor.temperature())