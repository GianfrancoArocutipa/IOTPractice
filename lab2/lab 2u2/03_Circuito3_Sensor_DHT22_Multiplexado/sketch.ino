// CIRCUITO 3: SENSOR DIGITAL DHT22 CON DISPLAY MULTIPLEXADO - ARDUINO NANO
// Muestra la temperatura en tiempo real en los 2 displays (00 a 99 °C)
// y envía temperatura y humedad al Monitor Serial

#include "DHT.h"

#define DHTPIN 11      // Pin conectado a la línea de datos (SDA) del DHT22
#define DHTTYPE DHT22  // Sensor DHT22 (AM2302)

DHT dht(DHTPIN, DHTTYPE);

// Pines de segmentos a, b, c, d, e, f, g en Arduino Nano
const byte segmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de habilitación a la base de los transistores 2N2222
const byte display1 = 9;   // Decenas (Display Izquierdo, col 22)
const byte display2 = 10;  // Unidades (Display Derecho, col 28)

// Tabla de segmentos para cátodo común (1 = segmento encendido)
// a, b, c, d, e, f, g
const byte numeros[10][7] = {
  {1, 1, 1, 1, 1, 1, 0}, // 0
  {0, 1, 1, 0, 0, 0, 0}, // 1
  {1, 1, 0, 1, 1, 0, 1}, // 2
  {1, 1, 1, 1, 0, 0, 1}, // 3
  {0, 1, 1, 0, 0, 1, 1}, // 4
  {1, 0, 1, 1, 0, 1, 1}, // 5
  {1, 0, 1, 1, 1, 1, 1}, // 6
  {1, 1, 1, 0, 0, 0, 0}, // 7
  {1, 1, 1, 1, 1, 1, 1}, // 8
  {1, 1, 1, 1, 0, 1, 1}  // 9
};

int tempMostrar = 24;            // Temperatura mostrada por defecto
unsigned long ultimoMuestreo = 0;
const unsigned long INTERVALO_DHT = 1500; // Leer sensor cada 1.5 s

void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
    digitalWrite(segmentos[i], LOW);
  }

  pinMode(display1, OUTPUT);
  pinMode(display2, OUTPUT);
  digitalWrite(display1, LOW);
  digitalWrite(display2, LOW);

  Serial.begin(9600);
  dht.begin();
  Serial.println(F("============================================="));
  Serial.println(F(" SISTEMA DE TEMPERATURA Y HUMEDAD DHT22 "));
  Serial.println(F(" Escuela de Ingenieria de Sistemas - UPT "));
  Serial.println(F("============================================="));
}

void mostrarNumero(byte numero) {
  if (numero > 9) numero = 0;
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], numeros[numero][i]);
  }
}

void refrescarMultiplexado(int valor) {
  if (valor < 0) valor = 0;
  if (valor > 99) valor = 99;

  byte decenas = valor / 10;
  byte unidades = valor % 10;

  // 1. Mostrar Decenas en Display 1 (Izquierdo)
  digitalWrite(display2, LOW);   // Apagar unidades
  mostrarNumero(decenas);        // Cargar segmentos de decenas
  digitalWrite(display1, HIGH);  // Encender transistor decenas
  delay(4);                      // Persistencia visual (4 ms)
  digitalWrite(display1, LOW);   // Apagar decenas

  // 2. Mostrar Unidades en Display 2 (Derecho)
  mostrarNumero(unidades);       // Cargar segmentos de unidades
  digitalWrite(display2, HIGH);  // Encender transistor unidades
  delay(4);                      // Persistencia visual (4 ms)
  digitalWrite(display2, LOW);   // Apagar unidades
}

void loop() {
  // Tarea 1: Lectura no bloqueante del sensor cada 1.5 s
  unsigned long tiempoActual = millis();
  if (tiempoActual - ultimoMuestreo >= INTERVALO_DHT) {
    ultimoMuestreo = tiempoActual;
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (!isnan(t) && !isnan(h)) {
      tempMostrar = (int)round(t);
      Serial.print(F("[DHT22] Temp: "));
      Serial.print(t, 1);
      Serial.print(F(" C | Humedad: "));
      Serial.print(h, 1);
      Serial.print(F(" % | Display 7-Seg: "));
      Serial.println(tempMostrar);
    } else {
      Serial.println(F("[ERROR] Fallo al leer datos del sensor DHT22"));
    }
  }

  // Tarea 2: Refresco continuo sin parpadeo (frecuencia ~125 Hz)
  refrescarMultiplexado(tempMostrar);
}