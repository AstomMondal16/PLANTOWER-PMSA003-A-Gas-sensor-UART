#ifndef PMSA003_H
#define PMSA003_H

#include <Arduino.h>

struct PmsaData {
    uint16_t pm10_cf1;
    uint16_t pm25_cf1;
    uint16_t pm100_cf1;
};

void pmsa003_init(uint8_t txPin, uint8_t rxPin);
bool pmsa003_read(PmsaData &data);

#endif // PMSA003_H
