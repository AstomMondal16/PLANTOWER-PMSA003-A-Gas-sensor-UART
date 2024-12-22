#include <stdio.h>
#include <string.h>
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "pmsa003.h"

#define TAG "PMSA003"


// Initialize UART
void pmsa003_init(pmsa003_t *sensor, int tx_pin, int rx_pin) {
    const uart_config_t uart_config = {
        .baud_rate = 9600,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    ESP_ERROR_CHECK(uart_param_config(UART_NUM, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_NUM, tx_pin, rx_pin, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(UART_NUM, BUF_SIZE * 2, 0, 0, NULL, 0));
    sensor->uart_port = UART_NUM;
}

// Verify checksum
static esp_err_t verify_checksum(const uint8_t *data, size_t len) {
    uint16_t sum = 0;
    for (size_t i = 0; i < len - 2; i++) {
        sum += data[i];
    }
    uint16_t sent = (data[len - 2] << 8) | data[len - 1];
    return (sum == sent) ? ESP_OK : ESP_FAIL;
}

// Read sensor data
esp_err_t pmsa003_read(pmsa003_t *sensor, pmsa003_data_t *data) {
    uint8_t buf[32] = {0};
    int len = uart_read_bytes(sensor->uart_port, buf, sizeof(buf), pdMS_TO_TICKS(sensor->timeout_ms));
    if (len < 32) {
        ESP_LOGE(TAG, "Failed to read complete frame");
        return ESP_FAIL;
    }

    if (buf[0] != 0x42 || buf[1] != 0x4D) {
        ESP_LOGE(TAG, "Invalid frame header");
        return ESP_FAIL;
    }

    if (verify_checksum(buf, len) != ESP_OK) {
        ESP_LOGE(TAG, "Checksum validation failed");
        return ESP_FAIL;
    }

    data->pm10_cf1 = (buf[4] << 8) | buf[5];
    data->pm25_cf1 = (buf[6] << 8) | buf[7];
    data->pm100_cf1 = (buf[8] << 8) | buf[9];
    return ESP_OK;
}

// Deinitialize UART
void pmsa003_deinit(pmsa003_t *sensor) {
    uart_driver_delete(sensor->uart_port);
}
