import yaml
from types_.ctd import CTD
from types_.sensors.generic import GenericSensor

# from atlas_i2c import commands, sensors, atlas_i2c

if __name__ == '__main__':
    atlas_sensors = []
    bluerobotics_sensors = []

    ctd = CTD(config_path="config.yaml")
    # ctd.setup_sensors()
    #
    # print(ctd.sensors)

    # if "atlas-sensors" in cfg:
    #     for sensor_cfg in cfg["atlas-sensors"]:
    #         sensor = sensors.Sensor(cfg["atlas-sensors"][sensor_cfg]["name"],
    #                                 cfg["atlas-sensors"][sensor_cfg]["address"])
    #         atlas_sensors.append(sensor)
    #
    # if "bluerobotics-sensors" in cfg:
    #     for sensor_cfg in cfg["bluerobotics-sensors"]:
    #         # sensor = sensors.Sensor(cfg["bluerobotics-sensors"][sensor_cfg]["name"], cfg["bluerobotics-sensors"][sensor_cfg]["address"])
    #         import ms5837
    #
    #         # https://github.com/bluerobotics/ms5837-python
    #         sensor = ms5837.MS5837()  # Use defaults (MS5837-30BA device on I2C bus 1)
    #         bluerobotics_sensors.append(sensor)

    # while True:
    #     for sensor in atlas_sensors:
    #         sensor.connect()
    #         response = sensor.query(commands.READ)
    #         print(f"Data for {sensor.name}: {response.data}")
    #
    #     for sensor in bluerobotics_sensors:
    #         sensor.init()
    #         sensor.read(ms5837.OSR_256)
