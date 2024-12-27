import pmsa003
import time

def main():
    sensor_port = "/dev/serial0"  # Adjust for your setup, e.g., `/dev/ttyUSB0`
    try:
        # Initialize PMSA003 sensor
        sensor = pmsa003.Sensor(port=sensor_port)

        while True:
            try:
                # Read sensor data
                pmsa003_data = sensor.read()

                # Print PM1.0, PM2.5, PM10 (CF1 values)
                print(f"PM1.0: {pmsa003_data.pm10_cf1}, PM2.5: {pmsa003_data.pm25_cf1}, PM10: {pmsa003_data.pm100_cf1}")

                time.sleep(5)  # Wait for 5 seconds before the next reading
            except pmsa003.SensorException as e:
                print(f"Error reading sensor: {e}")

    except Exception as e:
        print(f"Error initializing PMSA003 sensor: {e}")
    finally:
        if 'sensor' in locals():
            sensor.close()

if __name__ == "__main__":
    main()

