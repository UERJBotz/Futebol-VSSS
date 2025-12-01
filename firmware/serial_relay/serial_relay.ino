#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>  //! checar se precisa mesmo
#include <Wire.h> //! checar se precisa mesmo
#include "../comms.h"

#define BAUD_RATE 115200
#define FONTE u8g2_font_missingplanet_tf
//choose a suitable font at https://github.com/olikraus/u8g2/wiki/fntlistall

uint8_t peer_addr[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C oled(U8G2_R2);


void setup() {
    init_wifi();
    uint8_t* mac_addr = get_mac_addr();

    Serial.begin(BAUD_RATE);
    Serial.printf("MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                  mac_addr[0], mac_addr[1], mac_addr[2],
                  mac_addr[3], mac_addr[4], mac_addr[5]);

    static esp_now_peer_info_t peer {
        .channel = 0,
        .encrypt = false,
    };
    memcpy(peer.peer_addr, peer_addr, sizeof(peer_addr));

    esp_err_t err = esp_now_add_peer(&peer);
    assert (err == ESP_OK);

    oled.begin();
    oled.setFont(FONTE);

    oled.clearBuffer();            // clear the internal memory
    oled.drawStr(10,29, "ligado"); // write something to the internal memory
    oled.sendBuffer();             // transfer internal memory to the display
}

unsigned long last_pkg_sent = 0;
void loop() {
    static char input[256];
    static const char sentinel = '\n';

    if (millis() - last_pkg_sent < 50) return;
    for (auto buf = input; Serial.available(); buf++) {
        *buf = (char) Serial.read();
        if (*buf == sentinel) {
            *buf = '\0';
            Packet msg {
                .id = 0,
                .len  = strlen(input),
            };
            strcpy(msg.vels, input);
            Serial.println(input); //! print

            esp_err_t err = esp_now_send(peer_addr, (uint8_t*) &msg, sizeof(msg));
            if (err == ESP_OK) Serial.println("Sent with success");
            else               Serial.println("Error sending the data");
            last_pkg_sent = millis();
        }
    }
    // esse loop lê da serial até encontrar um \n e aí faz broadcast via espnow
    // se a mensagem parar de chegar antes disso, ele ignora
    // detalhe: Serial.available() retorna quantos bytes tão disponíveis

    if (last_pkg_sent) {
        oled.clearBuffer();
        oled.drawStr(1,10, input);
        oled.sendBuffer();
    }
}
