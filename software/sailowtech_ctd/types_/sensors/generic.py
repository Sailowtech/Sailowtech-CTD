class GenericSensor:
    def __init__(self, name: str, address: int):
        self.name = name
        self.addr = address

    def read_value(self):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'name="{self.name}", ' \
               f'address={hex(self.addr)}' \
               f')'

    def __repr__(self):
        return self.__str__()
