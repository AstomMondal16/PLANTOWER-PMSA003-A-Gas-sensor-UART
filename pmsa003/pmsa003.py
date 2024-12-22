"""
Interface to read from the Plantower PMS A003 sensor.
"""
from machine import UART
import time

# Constants
DEFAULT_SERIAL_PORT = 1  # UART2
DEFAULT_READ_TIMEOUT = 2  # Timeout in seconds


class SensorReading:
    """One single reading from the PMS A003 sensor."""

    def __init__(self, line):
        self.pm10_cf1 = line[4] * 256 + line[5]
        self.pm25_cf1 = line[6] * 256 + line[7]
        self.pm100_cf1 = line[8] * 256 + line[9]
        self.pm10_std = line[10] * 256 + line[11]
        self.pm25_std = line[12] * 256 + line[13]
        self.pm100_std = line[14] * 256 + line[15]
        self.gr03um = line[16] * 256 + line[17]
        self.gr05um = line[18] * 256 + line[19]
        self.gr10um = line[20] * 256 + line[21]
        self.gr25um = line[22] * 256 + line[23]
        self.gr50um = line[24] * 256 + line[25]
        self.gr100um = line[26] * 256 + line[27]


class SensorException(Exception):
    """Custom exception for sensor errors."""
    pass


class Sensor:
    """The interface class for the PMS A003 sensor."""

    def __init__(self, port=DEFAULT_SERIAL_PORT, read_timeout=DEFAULT_READ_TIMEOUT, tx=11, rx=12):
        self.port = port
        self.read_timeout = read_timeout
        try:
            self.serial = UART(self.port, baudrate=9600, tx=tx, rx=rx, bits=8, parity=None, stop=1)
        except Exception as e:
            raise SensorException(f"Failed to initialize UART: {str(e)}")

    def _verify(self, recv):
        """Verify the checksum of the data."""
        calc = sum(bytearray(recv[:-2]))
        sent = (recv[-2] << 8) | recv[-1]
        if sent != calc:
            raise SensorException("Checksum invalid")

    def read(self):
        """Read a new value from the sensor."""
        recv = b''
        timeout_time = time.time() + self.read_timeout

        while True:
            inp = self.serial.read(1)
            if not inp:  # Handle no data received
                if time.time() > timeout_time:
                    raise SensorException("No message received within timeout.")
                time.sleep(0.1)
                continue

            if inp == b'\x42':
                recv += inp
                inp = self.serial.read(1)
                if inp == b'\x4d':
                    recv += inp
                    recv += self.serial.read(30)
                    break

        self._verify(recv)
        return SensorReading(recv)

    def deinit(self):
        """Deinitialize the sensor by closing the UART connection."""
        try:
            self.serial.deinit()

        except Exception as e:
            raise SensorException(f"Failed to deinitialize sensor: {str(e)}")
