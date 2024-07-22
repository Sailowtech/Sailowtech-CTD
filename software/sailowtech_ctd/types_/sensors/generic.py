class GenericSensor:
    def __init__(self, name: str, address: int):
        self.name = name
        self.addr = address

    def read_value(self):
        pass
