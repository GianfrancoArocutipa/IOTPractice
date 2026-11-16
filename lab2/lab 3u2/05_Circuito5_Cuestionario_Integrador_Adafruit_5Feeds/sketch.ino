// CIRCUITO 5: CUESTIONARIO INTEGRAL - 5 FEEDS EN ADAFRUIT IO
// Publica: Temperatura, Humedad, Sensación Térmica, Potenciómetro 1 y Potenciómetro 2
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "gianfranco_arocutipa"
#define AIO_KEY         "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx"

#define DHTPIN          13
#define DHTTYPE         DHT22
const int pinPot1     = 34; // Potenciómetro 1 (ADC1 - Canal 6)
const int pinPot2     = 35; // Potenciómetro 2 (ADC1 - Canal 7)

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// 5 Feeds configurados en Adafruit IO
Adafruit_MQTT_Publish feedTemp     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/temperatura");
Adafruit_MQTT_Publish feedHum      = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/humedad");
Adafruit_MQTT_Publish feedSensTerm = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/sensacion-termica");
Adafruit_MQTT_Publish feedPot1     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/potenciometro-1");
Adafruit_MQTT_Publish feedPot2     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/potenciometro-2");

DHT dht(DHTPIN, DHTTYPE);

void conectarMQTT();

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Iniciando conexión WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[WiFi] Conectado exitosamente");
}

void loop() {
  conectarMQTT();

  // 1. Lecturas de DHT22
  float h = dht.readHumidity();
  float tc = dht.readTemperature();
  if (!isnan(h) && !isnan(tc)) {
    float st = dht.computeHeatIndex(tc, h, false);
    Serial.println("[DHT22] Temp: " + String(tc, 1) + " °C | Hum: " + String(h, 1) + " % | ST: " + String(st, 1) + " °C");
    feedTemp.publish(tc);
    feedHum.publish(h);
    feedSensTerm.publish(st);
  }

  // 2. Potenciómetro 1 (GPIO 34 - ADC1)
  int val1 = analogRead(pinPot1);
  float vol1 = val1 * 3.3 / 4095.0;
  Serial.println("[POT 1] ADC: " + String(val1) + " | Voltaje: " + String(vol1, 2) + " V");
  feedPot1.publish(vol1);

  // 3. Potenciómetro 2 (GPIO 35 - ADC1)
  int val2 = analogRead(pinPot2);
  float vol2 = val2 * 3.3 / 4095.0;
  Serial.println("[POT 2] ADC: " + String(val2) + " | Voltaje: " + String(vol2, 2) + " V");
  feedPot2.publish(vol2);

  Serial.println("-> 5 Feeds transmitidos a Adafruit IO. Próximo ciclo en 7s...");
  Serial.println("----------------------------------------------------------------");
  delay(7000);
}

void conectarMQTT() {
  int8_t ret;
  if (mqtt.connected()) return;

  Serial.print("Conectando con Adafruit IO MQTT... ");
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Reintentando en 5 segundos...");
    mqtt.disconnect();
    delay(5000);
  }
  Serial.println("¡Conectado exitosamente!");
}
