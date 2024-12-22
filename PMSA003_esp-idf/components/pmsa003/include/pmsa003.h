#ifndef PMSA003_H
#define PMSA003_H

#include "esp_err.h"

#define PMSA003_TX_PIN 11
#define PMSA003_RX_PIN 12
#define UART_NUM UART_NUM_1
#define BUF_SIZE 128

typedef struct {
    int uart_port;
    int timeout_ms;
} pmsa003_t;

typedef struct {
    uint16_t pm10_cf1;
    uint16_t pm25_cf1;
    uint16_t pm100_cf1;
} pmsa003_data_t;

void pmsa003_init(pmsa003_t *sensor, int tx_pin, int rx_pin);
esp_err_t pmsa003_read(pmsa003_t *sensor, pmsa003_data_t *data);
void pmsa003_deinit(pmsa003_t *sensor);

#endif // PMSA003_H
