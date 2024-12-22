#include <stdio.h>
#include "pmsa003.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"


void app_main(void) {

    while (1) {
        pmsa003_t sensor = {.timeout_ms = 2000};
        pmsa003_init(&sensor, PMSA003_TX_PIN, PMSA003_RX_PIN);

        pmsa003_data_t data;
        if (pmsa003_read(&sensor, &data) == ESP_OK) {
            printf("PM1.0: %d, PM2.5: %d, PM10: %d\n", data.pm10_cf1, data.pm25_cf1, data.pm100_cf1);
        } else {
            printf("Failed to read sensor data\n");
        }
        pmsa003_deinit(&sensor);
        vTaskDelay(pdMS_TO_TICKS(10000));
    }

    
}
