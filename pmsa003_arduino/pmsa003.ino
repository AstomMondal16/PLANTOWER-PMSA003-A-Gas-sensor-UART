#include <Arduino.h>
#include "pmsa003.h"

#define PMSA003_TX_PIN 1	//adjust the TX pin of the sensor
#define PMSA003_RX_PIN 1	//adjust the RX pin of the sensor

void setup() {
    Serial.begin(115200);
    pmsa003_init(PMSA003_TX_PIN, PMSA003_RX_PIN);
    Serial.println("PMSA003A sensor initialized");
}

void loop() {
    PmsaData data;
    if (pmsa003_read(data)) {
        Serial.printf("PM1.0: %d, PM2.5: %d, PM10: %d\n", data.pm10_cf1, data.pm25_cf1, data.pm100_cf1);
    } else {
        Serial.println("Failed to read sensor data");
    }

    delay(10000); // Wait for 10 seconds
}
