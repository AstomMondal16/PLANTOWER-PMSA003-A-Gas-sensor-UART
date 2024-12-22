#include "pmsa003.h"

HardwareSerial pmsaSerial(2);

void pmsa003_init(uint8_t txPin, uint8_t rxPin) {
    pmsaSerial.begin(9600, SERIAL_8N1, rxPin, txPin);
}

bool verify_checksum(const uint8_t *data, size_t len) {
    uint16_t sum = 0;
    for (size_t i = 0; i < len - 2; i++) {
        sum += data[i];
    }
    uint16_t sent = (data[len - 2] << 8) | data[len - 1];
    return sum == sent;
}

bool pmsa003_read(PmsaData &data) {
    uint8_t buf[32] = {0};
    if (pmsaSerial.available() >= 32) {
        pmsaSerial.readBytes(buf, 32);

        if (buf[0] != 0x42 || buf[1] != 0x4D) {
            return false; // Invalid frame header
        }

        if (!verify_checksum(buf, 32)) {
            return false; // Checksum validation failed
        }

        data.pm10_cf1 = (buf[4] << 8) | buf[5];
        data.pm25_cf1 = (buf[6] << 8) | buf[7];
        data.pm100_cf1 = (buf[8] << 8) | buf[9];
        return true;
    }

    return false; // Insufficient data
}
