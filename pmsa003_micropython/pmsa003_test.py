from machine import UART, Pin, I2C
import pmsa003
import time

while True:
    try:
        
        # Read PMSA003 sensor
        sensor = pmsa003.Sensor(1)
        pmsa003_data = sensor.read()
        print(f"PM1.0: {pmsa003_data.pm10_cf1}, PM2.5: {pmsa003_data.pm25_cf1}, PM10: {pmsa003_data.pm100_cf1}")
        time.sleep(0.5)
        sensor.deinit()
        
    except Exception as e:
        print(f"Error reading PMSA003 sensor: {e}")
        pmsa003_data = pmsa003.SensorReading([0] * 32)

