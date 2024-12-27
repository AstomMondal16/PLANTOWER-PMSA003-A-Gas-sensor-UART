"""
Interface to read from the Plantower PMS A003 sensor on Raspberry Pi.
"""
import serial
import time

class SensorReading:
    """Represents a single reading from the PMS A003 sensor."""

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

    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=2):
        try:
            self.serial = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        except Exception as e:
            raise SensorException(f"Failed to initialize serial port: {str(e)}")

    def _verify(self, recv):
        """Verify the checksum of the data."""
        calc = sum(recv[:-2])
        sent = (recv[-2] << 8) | recv[-1]
        if sent != calc:
            raise SensorException("Checksum invalid")

    def read(self):
        """Read a new value from the sensor."""
        recv = b''
        start_time = time.time()

        while True:
            byte = self.serial.read(1)
            if not byte:
                if time.time() - start_time > self.serial.timeout:
                    raise SensorException("No message received within timeout.")
                continue

            if byte == b'\x42':  # Start byte
                recv += byte
                byte = self.serial.read(1)
                if byte == b'\x4d':  # Second start byte
                    recv += byte
                    recv += self.serial.read(30)  # Read the remaining data
                    break

        self._verify(recv)
        return SensorReading(recv)

    def close(self):
        """Deinitialize the sensor by closing the serial connection."""
        try:
            self.serial.close()
        except Exception as e:
            raise SensorException(f"Failed to close serial port: {str(e)}")
