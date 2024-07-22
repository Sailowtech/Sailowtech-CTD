from software.sailowtech_ctd.types_.sensors.generic import GenericSensor


class AtlasSensor(GenericSensor):
    def __init__(self, name: str, address: int):
        super().__init__(name, address)
