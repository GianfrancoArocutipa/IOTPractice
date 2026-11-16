// CIRCUITO 3: SENSOR DHT22 Y POTENCIÓMETRO ANALÓGICO - ESP32
#include "DHT.h"

#define pin1 13        // GPIO 13 -> Datos DHT22
int pin2 = 34;         // GPIO 34 -> Potenciómetro (ADC1_CH6)

DHT dht(pin1, DHT22);

void setup() {
  Serial.begin(115200);
  Serial.println("Test de sensores:");
  dht.begin();
}

void loop() {
  delay(500);
  leerdht();
  delay(500);
  leerpot();
}

void leerdht() {
  float h = dht.readHumidity();
  float tc = dht.readTemperature();
  float tf = dht.readTemperature(true);
  float st = dht.computeHeatIndex(tc, h, false);

  Serial.println("Temperatura: " + String(tc) + " °C");
  Serial.println("Humedad: " + String(h) + " %");
  Serial.println("Temperatura: " + String(tf) + " °F");
  Serial.println("Sensación Térmica: " + String(st) + " °C");
  Serial.println("--------------------------------------------");
  delay(2000);
}

void leerpot() {
  int potValor = analogRead(pin2);
  float vol = potValor * 3.3 / 4095.0;
  Serial.println("Lectura ADC: " + String(potValor) + " binario");
  Serial.println("Voltaje: " + String(vol, 2) + " V");
  Serial.println("--------------------------------------------");
  delay(500);
}
