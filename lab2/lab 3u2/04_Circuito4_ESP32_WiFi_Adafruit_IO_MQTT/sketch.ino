// CIRCUITO 4: ESP32 + WIFI + ADAFRUIT IO (MQTT)
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// Configuración WiFi Wokwi
#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

// Servidor y Credenciales Adafruit IO
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "gianfranco_arocutipa"
#define AIO_KEY         "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx"

#define DHTPIN          13
#define DHTTYPE         DHT22
int pin2 = 34;          // GPIO 34 (ADC1_CH6)

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// Feeds en Adafruit IO
Adafruit_MQTT_Publish temperatura = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/DHT22");
Adafruit_MQTT_Publish voltaje     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Potenciometro");

DHT dht(DHTPIN, DHTTYPE);

void conectarMQTT();

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Conectando WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado exitosamente");
}

void loop() {
  conectarMQTT();
  leerdht();
  leerpot();
  Serial.println("Datos enviados a Adafruit IO");
  Serial.println("--------------------------------");
  delay(7000);
}

void leerdht() {
  float tc = dht.readTemperature();
  if (!isnan(tc)) {
    Serial.println("Temperatura : " + String(tc) + " °C");
    temperatura.publish(tc);
  }
}

void leerpot() {
  int lectura = analogRead(pin2);
  float vol = lectura * 3.3 / 4095.0;
  Serial.println("ADC      : " + String(lectura));
  Serial.println("Voltaje  : " + String(vol) + " V");
  voltaje.publish(vol);
}

void conectarMQTT() {
  int8_t ret;
  if (mqtt.connected()) return;

  Serial.print("Conectando a Adafruit IO... ");
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Reintentando en 5 segundos...");
    mqtt.disconnect();
    delay(5000);
  }
  Serial.println("Conectado");
}
