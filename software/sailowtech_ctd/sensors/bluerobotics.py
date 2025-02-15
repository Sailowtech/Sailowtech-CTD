from time import sleep
import smbus2 as smbus

from software.sailowtech_ctd.sensors.generic import GenericSensor, SensorBrand
from .types import Sensor, Metric


class BlueRoboticsSensor(GenericSensor):
    """
    Base for a Bluerobotics sensor
    """
    def __init__(self, sensor: Sensor, name: str, address: int, min_delay: float):
        super().__init__(SensorBrand.BlueRobotics, sensor, name, address, min_delay, Metric.DEPTH)


class DepthSensor(BlueRoboticsSensor):
    """
    Class for a depth sensor by Bluerobotics
    """
    _MS5837_ADDR = 0x76
    _MS5837_RESET = 0x1E
    _MS5837_ADC_READ = 0x00
    _MS5837_PROM_READ = 0xA0
    _MS5837_CONVERT_D1_256 = 0x40
    _MS5837_CONVERT_D2_256 = 0x50

    DEFAULT_ADDRESS = 98

    # Models
    MODEL_02BA = 0
    MODEL_30BA = 1

    # Oversampling options
    OSR_256 = 0
    OSR_512 = 1
    OSR_1024 = 2
    OSR_2048 = 3
    OSR_4096 = 4
    OSR_8192 = 5

    # kg/m^3 convenience
    DENSITY_FRESHWATER = 997
    DENSITY_SALTWATER = 1029

    # Conversion factors (from native unit, mbar)
    UNITS_Pa = 100.0
    UNITS_hPa = 1.0
    UNITS_kPa = 0.1
    UNITS_mbar = 1.0
    UNITS_bar = 0.001
    UNITS_atm = 0.000986923
    UNITS_Torr = 0.750062
    UNITS_psi = 0.014503773773022

    # Valid units
    UNITS_Centigrade = 1
    UNITS_Fahrenheit = 2
    UNITS_Kelvin = 3

    def __init__(self, name: str, address: int = DEFAULT_ADDRESS, min_delay: float = 1):
        """
        Initialise the class of the depth sensor
        :param name: Name of the sensor
        :param address: I2C-Address of the sensor
        :param min_delay: Required minimum delay
        """
        super().__init__(Sensor.BLUEROBOTICS_BAR30_DEPTH, name, address, min_delay)
        self._model = self.MODEL_30BA
        self._C = []

        self._fluidDensity = self.DENSITY_FRESHWATER
        self._pressure = 0
        self._temperature = 0
        self._D1 = 0
        self._D2 = 0

    def init(self, bus: smbus.SMBus) -> bool:
        """
        Initialise the device of the depth sensor
        :param bus: SMBus over which the device can be reached
        :return: True if successful
        """
        bus.write_byte(i2c_addr=self._MS5837_ADDR, value=self._MS5837_RESET)

        # Wait for reset to complete
        sleep(0.01)

        self._C = []

        # Read calibration values and CRC
        for i in range(7):
            c = bus.read_word_data(self._MS5837_ADDR, self._MS5837_PROM_READ + 2 * i)
            c = ((c & 0xFF) << 8) | (c >> 8)  # SMBus is little-endian for word transfers, we need to swap MSB and LSB
            self._C.append(c)

        crc = (self._C[0] & 0xF000) >> 12
        if crc != self._crc4(self._C):
            print("PROM read error, CRC failed!")
            return False
        return True

    def write_read_command(self, bus: smbus.SMBus) -> bool:
        return True

    def read_result(self, bus: smbus.SMBus) -> float:
        return self.measure_value(bus)

    def measure_value(self, bus: smbus.SMBus) -> float:
        """
        Measures the different values
        :param bus: SMBus over which the device can be reached
        :return: Returns the different values
        """
        self.read(bus)
        # TODO here, we are returning all the different values that we get from this sensor. However, we are only expecting one. We need to find a good solution on how to differentiate these readings across the objects. Maybe save both depth and pressure, since both can be useful and directly saving the depth can be good for easier quick-assessment
        return self.depth()

    ###############################################################
    # FULLY COPIED FROM BLUEROBOTICS's CODE, just some parameters adapted and "self."  added
    def read(self, bus: smbus.SMBus, oversampling=OSR_8192) -> bool:
        """
        Take a reading of the sensor
        :param bus: SMBus over which the device can be reached
        :param oversampling: Oversampling attribute
        :return: True if successful
        """
        if oversampling < self.OSR_256 or oversampling > self.OSR_8192:
            print("Invalid oversampling option!")
            return False

        # Request D1 conversion (pressure)
        bus.write_byte(self._MS5837_ADDR, self._MS5837_CONVERT_D1_256 + 2 * oversampling)

        # Maximum conversion time increases linearly with oversampling
        # max time (seconds) ~= 2.2e-6(x) where x = OSR = (2^8, 2^9, ..., 2^13)
        # We use 2.5e-6 for some overhead
        sleep(2.5e-6 * 2 ** (8 + oversampling))

        d = bus.read_i2c_block_data(self._MS5837_ADDR, self._MS5837_ADC_READ, 3)
        self._D1 = d[0] << 16 | d[1] << 8 | d[2]

        # Request D2 conversion (temperature)
        bus.write_byte(self._MS5837_ADDR, self._MS5837_CONVERT_D2_256 + 2 * oversampling)

        # As above
        sleep(2.5e-6 * 2 ** (8 + oversampling))

        d = bus.read_i2c_block_data(self._MS5837_ADDR, self._MS5837_ADC_READ, 3)
        self._D2 = d[0] << 16 | d[1] << 8 | d[2]

        # Calculate compensated pressure and temperature
        # using raw ADC values and internal calibration
        self._calculate()

        return True

    def set_fluid_density(self, density):
        """
        Set the fluid density of the water
        :param density: Density to be set
        :return: None
        """
        self._fluidDensity = density

    def pressure(self, conversion=UNITS_mbar) -> float:
        """
        Get the pressure in the requested unit. Defaults to mBar.
        :param conversion: The unit conversion which should be used to return the value
        :return: Returns the pressure measured
        """
        return self._pressure * conversion


    def temperature(self, conversion=UNITS_Centigrade) -> float:
        """
        Temperature in requested units. Default in degrees Celsius
        :param conversion: The conversion to be applied
        :return: Returns the temperature in requested unit
        """
        deg_c = self._temperature / 100.0
        if conversion == self.UNITS_Fahrenheit:
            return (9.0 / 5.0) * deg_c + 32
        elif conversion == self.UNITS_Kelvin:
            return deg_c + 273
        return deg_c


    def depth(self) -> float:
        """
        Depth relative to MSL pressure in given fluid density
        :return: Returns depth
        """
        return (self.pressure(self.UNITS_Pa) - 101300) / (self._fluidDensity * 9.80665)


    def altitude(self) -> float:
        """
        Altitude relative to MSL pressure
        :return: Altitude relative to MSL pressure
        """
        return (1 - pow((self.pressure() / 1013.25), .190284)) * 145366.45 * .3048

        # Cribbed from datasheet

    def _calculate(self) -> None:
        OFFi = 0
        SENSi = 0
        Ti = 0

        dT = self._D2 - self._C[5] * 256
        if self._model == self.MODEL_02BA:
            SENS = self._C[1] * 65536 + (self._C[3] * dT) / 128
            OFF = self._C[2] * 131072 + (self._C[4] * dT) / 64
            self._pressure = (self._D1 * SENS / (2097152) - OFF) / (32768)
        else:
            SENS = self._C[1] * 32768 + (self._C[3] * dT) / 256
            OFF = self._C[2] * 65536 + (self._C[4] * dT) / 128
            self._pressure = (self._D1 * SENS / (2097152) - OFF) / (8192)

        self._temperature = 2000 + dT * self._C[6] / 8388608

        # Second order compensation
        if self._model == self.MODEL_02BA:
            if (self._temperature / 100) < 20:  # Low temp
                Ti = (11 * dT * dT) / (34359738368)
                OFFi = (31 * (self._temperature - 2000) * (self._temperature - 2000)) / 8
                SENSi = (63 * (self._temperature - 2000) * (self._temperature - 2000)) / 32

        else:
            if (self._temperature / 100) < 20:  # Low temp
                Ti = (3 * dT * dT) / (8589934592)
                OFFi = (3 * (self._temperature - 2000) * (self._temperature - 2000)) / 2
                SENSi = (5 * (self._temperature - 2000) * (self._temperature - 2000)) / 8
                if (self._temperature / 100) < -15:  # Very low temp
                    OFFi = OFFi + 7 * (self._temperature + 1500) * (self._temperature + 1500)
                    SENSi = SENSi + 4 * (self._temperature + 1500) * (self._temperature + 1500)
            elif (self._temperature / 100) >= 20:  # High temp
                Ti = 2 * (dT * dT) / (137438953472)
                OFFi = (1 * (self._temperature - 2000) * (self._temperature - 2000)) / 16
                SENSi = 0

        OFF2 = OFF - OFFi
        SENS2 = SENS - SENSi

        if self._model == self.MODEL_02BA:
            self._temperature = (self._temperature - Ti)
            self._pressure = (((self._D1 * SENS2) / 2097152 - OFF2) / 32768) / 100.0
        else:
            self._temperature = (self._temperature - Ti)
            self._pressure = (((self._D1 * SENS2) / 2097152 - OFF2) / 8192) / 10.0

            # Cribbed from datasheet

    def _crc4(self, n_prom):
        """
        Checksum function
        :param n_prom: ?
        :return: Checksum
        """
        n_rem = 0

        n_prom[0] = ((n_prom[0]) & 0x0FFF)
        n_prom.append(0)

        for i in range(16):
            if i % 2 == 1:
                n_rem ^= ((n_prom[i >> 1]) & 0x00FF)
            else:
                n_rem ^= (n_prom[i >> 1] >> 8)

            for n_bit in range(8, 0, -1):
                if n_rem & 0x8000:
                    n_rem = (n_rem << 1) ^ 0x3000
                else:
                    n_rem = (n_rem << 1)

        n_rem = ((n_rem >> 12) & 0x000F)

        self.n_prom = n_prom
        self.n_rem = n_rem

        return n_rem ^ 0x00
