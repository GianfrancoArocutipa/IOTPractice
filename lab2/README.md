# Laboratorio 2.2: Arduino Nano, Displays de 7 Segmentos, Multiplexación y Sensor DHT22 en Wokwi

**Universidad Privada de Tacna**  
**Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas (IoT)  
**Docente:** Mgr. Alex Juan Yanqui Constancio  
**Autores:** Perez Fabrizio - Arocutipa Gian Franco  
**Documento base:** [Lab 2.2 Arduino Nano Wokwi.pdf](file:///c:/Users/PC/Desktop/oit/lab2/Lab%202.2%20Arduino%20Nano%20Wokwi.pdf)

---

## 🗂️ Estructura de Proyectos Wokwi Disponibles

Todos los circuitos ya se encuentran completamente montados y operativos en sus respectivas carpetas:

| Circuito | Descripción | Carpeta del Proyecto |
| :--- | :--- | :--- |
| **Circuito 1** | Contador de 0 a 9 en 1 Display de 7 Segmentos (Cátodo Común) | [01_Circuito1_Contador_0_9](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/01_Circuito1_Contador_0_9) |
| **Circuito 2** | Contador de 00 a 99 Multiplexado con 2 Displays y Transistores 2N2222 | [02_Circuito2_Contador_00_99_Multiplexado](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/02_Circuito2_Contador_00_99_Multiplexado) |
| **Circuito 3** | Sensor de Temperatura y Humedad DHT22 con Despliegue Multiplexado | [03_Circuito3_Sensor_DHT22_Multiplexado](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/03_Circuito3_Sensor_DHT22_Multiplexado) |

---

## ⚙️ Custom Chip Wokwi: Transistor NPN 2N2222 (Requerido para Circuitos 2 y 3)

Dado que Wokwi no incluye transistores BJT nativos en su paleta básica, se implementa mediante la **API de Custom Chips de Wokwi** (según la página 10 de la guía docente):

### `2n2222.chip.json`
```json
{
  "name": "2n2222",
  "author": "ALEX JUAN YANQUI CONSTANCIO",
  "pins": [
    "",
    "BASE",
    "EMI",
    "COL"
  ]
}
```

### `2n2222.chip.c`
```c
#include "wokwi-api.h"
#include <stdlib.h>

typedef struct {
  pin_t pin_base;
  pin_t pin_col;
  pin_t pin_emi;
} chip_state_t;

static void on_base_change(void *user_data, pin_t pin, uint32_t level) {
  chip_state_t *chip = (chip_state_t *)user_data;
  
  if (level == HIGH) {
    // Transistor en saturación: Conecta el colector a GND (nivel LOW)
    pin_mode(chip->pin_col, OUTPUT);
    pin_write(chip->pin_col, LOW); 
  } else {
    // Transistor en corte: Colector en alta impedancia (abierto)
    pin_mode(chip->pin_col, INPUT); 
  }
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_base = pin_init("BASE", INPUT);
  chip->pin_col = pin_init("COL", INPUT);
  chip->pin_emi = pin_init("EMI", INPUT);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = on_base_change,
    .user_data = chip,
  };
  pin_watch(chip->pin_base, &watch_config);
}
```

---

## 🔵 CIRCUITO 1: Contador de 0 a 9 en 1 Display de 7 Segmentos

### 1. Descripción del Montaje
Controla un display de 7 segmentos de cátodo común (`wokwi-7segment`). Los segmentos `a` hasta `g` se conectan mediante resistencias limitadoras de corriente de **$220\,\Omega$** a las salidas digitales **D2 hasta D8** del Arduino Nano. El cátodo común del display se habilita a través del pin **D10** (nivel ALTO enciende el display de unidades).

### 2. Tabla de Conexiones
| Señal | Pin Arduino Nano | Pin Display / Componente | Resistencia |
| :--- | :--- | :--- | :--- |
| Segmento `a` | `nano:2` | Pin `A` | $220\,\Omega$ |
| Segmento `b` | `nano:3` | Pin `B` | $220\,\Omega$ |
| Segmento `c` | `nano:4` | Pin `C` | $220\,\Omega$ |
| Segmento `d` | `nano:5` | Pin `D` | $220\,\Omega$ |
| Segmento `e` | `nano:6` | Pin `E` | $220\,\Omega$ |
| Segmento `f` | `nano:7` | Pin `F` | $220\,\Omega$ |
| Segmento `g` | `nano:8` | Pin `G` | $220\,\Omega$ |
| Control Cátodo | `nano:10` | Base Transistor Q2 $\rightarrow$ COM Unidades | $1\,\text{k}\Omega$ |
| Alimentación Protoboard | `nano:5V` $\rightarrow$ Bus `+` | `nano:GND.1` $\rightarrow$ Bus `-` | Directo |

### 3. Código Fuente (`sketch.ino`)
👉 Archivo: [01_Circuito1_Contador_0_9/sketch.ino](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/01_Circuito1_Contador_0_9/sketch.ino)

```cpp
// CIRCUITO 1: CONTADOR 0 A 9 EN 1 DISPLAY DE 7 SEGMENTOS
// Adaptado para el montaje con transistores (habilita solo el display de unidades en Pin 10)

int a = 2;
int b = 3;
int c = 4;
int d = 5;
int e = 6;
int f = 7;
int g = 8;
int tiempo = 600; // Retardo entre números (600 ms)

const int pinTransistorUnidades = 10; // Habilita el display derecho (sevseg1)
const int pinTransistorDecenas  = 9;  // Mantiene apagado el display izquierdo (sevseg2)

void setup() {
  pinMode(a, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(c, OUTPUT);
  pinMode(d, OUTPUT);
  pinMode(e, OUTPUT);
  pinMode(f, OUTPUT);
  pinMode(g, OUTPUT);

  pinMode(pinTransistorUnidades, OUTPUT);
  pinMode(pinTransistorDecenas, OUTPUT);

  digitalWrite(pinTransistorUnidades, HIGH); // Display derecho ENCENDIDO
  digitalWrite(pinTransistorDecenas, LOW);   // Display izquierdo APAGADO
}

void loop() {
  // Cero (0)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 1); digitalWrite(f, 1); digitalWrite(g, 0);
  delay(tiempo);

  // Uno (1)
  digitalWrite(a, 0); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 0); digitalWrite(e, 0); digitalWrite(f, 0); digitalWrite(g, 0);
  delay(tiempo);

  // Dos (2)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 0);
  digitalWrite(d, 1); digitalWrite(e, 1); digitalWrite(f, 0); digitalWrite(g, 1);
  delay(tiempo);

  // Tres (3)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 0); digitalWrite(f, 0); digitalWrite(g, 1);
  delay(tiempo);

  // Cuatro (4)
  digitalWrite(a, 0); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 0); digitalWrite(e, 0); digitalWrite(f, 1); digitalWrite(g, 1);
  delay(tiempo);

  // Cinco (5)
  digitalWrite(a, 1); digitalWrite(b, 0); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 0); digitalWrite(f, 1); digitalWrite(g, 1);
  delay(tiempo);

  // Seis (6)
  digitalWrite(a, 1); digitalWrite(b, 0); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 1); digitalWrite(f, 1); digitalWrite(g, 1);
  delay(tiempo);

  // Siete (7)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 0); digitalWrite(e, 0); digitalWrite(f, 0); digitalWrite(g, 0);
  delay(tiempo);

  // Ocho (8)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 1); digitalWrite(f, 1); digitalWrite(g, 1);
  delay(tiempo);

  // Nueve (9)
  digitalWrite(a, 1); digitalWrite(b, 1); digitalWrite(c, 1);
  digitalWrite(d, 1); digitalWrite(e, 0); digitalWrite(f, 1); digitalWrite(g, 1);
  delay(tiempo);
}
```

### 4. Esquemático Wokwi (`diagram.json`)
👉 Archivo: [01_Circuito1_Contador_0_9/diagram.json](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/01_Circuito1_Contador_0_9/diagram.json)

---

## 🟢 CIRCUITO 2: Contador de 00 a 99 Multiplexado con Transistores 2N2222

### 1. Descripción del Montaje y Técnica de Multiplexación
El circuito utiliza **dos displays de 7 segmentos de cátodo común compartiendo el mismo bus de datos (pines D2 a D8)**. 
- Para evitar que ambos displays muestren el mismo dígito al mismo tiempo, sus cátodos comunes están aislados y se conectan a tierra a través de dos transistores NPN 2N2222 actuando como interruptores digitales.
- **Pin D9 (Decenas):** Activa la base del transistor Q1 (display izquierdo).
- **Pin D10 (Unidades):** Activa la base del transistor Q2 (display derecho).
- **Persistencia de la Visión (POV):** Se alternan rápidamente las decenas y las unidades con un retardo de **$4\,\text{ms}$ por display**, alcanzando una frecuencia de refresco de $\approx 125\,\text{Hz}$, logrando una visualización simultánea continua libre de parpadeo.

### 2. Tabla de Conexiones
| Señal / Función | Pin Arduino Nano | Conexión en Protoboard |
| :--- | :--- | :--- |
| Bus de Segmentos `a..g` | `nano:2` a `nano:8` | A través de resistencias $220\,\Omega$ conectadas en paralelo a los segmentos `a..g` de ambos displays |
| Control Decenas | `nano:9` | Resistencia $1\,\text{k}\Omega \rightarrow$ Base Transistor Q1 (Colector a COM Display Izq, Emisor a GND) |
| Control Unidades | `nano:10` | Resistencia $1\,\text{k}\Omega \rightarrow$ Base Transistor Q2 (Colector a COM Display Der, Emisor a GND) |

### 3. Código Fuente (`sketch.ino`)
👉 Archivo: [02_Circuito2_Contador_00_99_Multiplexado/sketch.ino](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/02_Circuito2_Contador_00_99_Multiplexado/sketch.ino)

```cpp
// CIRCUITO 2: CONTADOR 00 A 99 MULTIPLEXADO - ARDUINO NANO
// Guía de Laboratorio 2.2 - Páginas 8, 9 y 10

const byte segmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de habilitación a la base de los transistores 2N2222
const byte display1 = 9;   // Decenas (Display Izquierdo)
const byte display2 = 10;  // Unidades (Display Derecho)

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

void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
    digitalWrite(segmentos[i], LOW);
  }

  pinMode(display1, OUTPUT);
  pinMode(display2, OUTPUT);

  digitalWrite(display1, LOW);
  digitalWrite(display2, LOW);
}

void mostrarNumero(byte numero) {
  if (numero > 9) numero = 0;
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], numeros[numero][i]);
  }
}

void mostrar(byte valor) {
  byte decenas = valor / 10;
  byte unidades = valor % 10;

  // 1. Mostrar Decenas en Display 1 (Izquierdo)
  digitalWrite(display2, LOW);   // Apagar unidades
  mostrarNumero(decenas);        // Enviar segmentos de decenas
  digitalWrite(display1, HIGH);  // Encender transistor decenas
  delay(4);                      // Persistencia visual (4 ms)
  digitalWrite(display1, LOW);   // Apagar decenas

  // 2. Mostrar Unidades en Display 2 (Derecho)
  mostrarNumero(unidades);       // Enviar segmentos de unidades
  digitalWrite(display2, HIGH);  // Encender transistor unidades
  delay(4);                      // Persistencia visual (4 ms)
  digitalWrite(display2, LOW);   // Apagar unidades
}

void loop() {
  // Cuenta de 00 a 99
  for (int i = 0; i < 100; i++) {
    // 100 iteraciones x 8 ms de refresco = ~800 ms por dígito
    for (int rep = 0; rep < 100; rep++) {
      mostrar(i);
    }
  }
}
```

### 4. Esquemático Wokwi (`diagram.json`)
👉 Archivo: [02_Circuito2_Contador_00_99_Multiplexado/diagram.json](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/02_Circuito2_Contador_00_99_Multiplexado/diagram.json)

---

## 🟣 CIRCUITO 3: Sensor Digital DHT22 con Despliegue en Displays Multiplexados

### 1. Descripción del Montaje
Integra un sensor digital de humedad y temperatura **DHT22** (`wokwi-dht22`) con el sistema de multiplexación de los dos displays:
- El pin de datos del DHT22 (`SDA`) se conecta al pin digital **D11** del Arduino Nano.
- El microcontrolador muestrea la temperatura cada **$1.5\,\text{segundos}$**, la descompone en decenas y unidades (ej. $24^\circ\text{C} \rightarrow$ Decena: $2$, Unidad: $4$) y la refresca dinámicamente en los displays mientras imprime los valores detallados por el puerto serie a $9600\,\text{baudios}$.

### 2. Tabla de Conexiones
| Componente | Pin Componente | Pin Arduino Nano / Bus | Función |
| :--- | :--- | :--- | :--- |
| **DHT22** | `VCC` | `nano:5V` (Bus `+`) | Alimentación 5V |
| | `SDA` | `nano:11` | Comunicación digital unifilar |
| | `GND` | `nano:GND.1` (Bus `-`) | Tierra común |
| **Bus de Segmentos** | `a..g` | `nano:2` a `nano:8` | Bus de datos de 7 segmentos |
| **Control Decenas** | Base Transistor Q1 | `nano:9` | Multiplexación Dígito Decenas |
| **Control Unidades**| Base Transistor Q2 | `nano:10` | Multiplexación Dígito Unidades |

### 3. Dependencias (`libraries.txt`)
```text
DHT sensor library
```

### 4. Código Fuente (`sketch.ino`)
👉 Archivo: [03_Circuito3_Sensor_DHT22_Multiplexado/sketch.ino](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/03_Circuito3_Sensor_DHT22_Multiplexado/sketch.ino)

```cpp
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
const byte display1 = 9;   // Decenas (Display Izquierdo)
const byte display2 = 10;  // Unidades (Display Derecho)

// Tabla de segmentos para cátodo común (1 = segmento encendido)
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

void refrescarDisplays(byte valor) {
  byte decenas = valor / 10;
  byte unidades = valor % 10;

  // Decenas
  digitalWrite(display2, LOW);
  mostrarNumero(decenas);
  digitalWrite(display1, HIGH);
  delay(4);
  digitalWrite(display1, LOW);

  // Unidades
  mostrarNumero(unidades);
  digitalWrite(display2, HIGH);
  delay(4);
  digitalWrite(display2, LOW);
}

void loop() {
  // Muestreo no bloqueante del sensor cada 1.5 segundos
  if (millis() - ultimoMuestreo >= INTERVALO_DHT) {
    ultimoMuestreo = millis();

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println(F("[ERROR] Fallo al leer el sensor DHT22. Verifique conexiones."));
    } else {
      tempMostrar = (int)t;
      if (tempMostrar < 0) tempMostrar = 0;
      if (tempMostrar > 99) tempMostrar = 99;

      Serial.print(F("Temperatura: "));
      Serial.print(t, 1);
      Serial.print(F(" °C  |  Humedad: "));
      Serial.print(h, 1);
      Serial.println(F(" %"));
    }
  }

  // Refrescar display multiplexado continuamente
  refrescarDisplays(tempMostrar);
}
```

### 5. Esquemático Wokwi (`diagram.json`)
👉 Archivo: [03_Circuito3_Sensor_DHT22_Multiplexado/diagram.json](file:///c:/Users/PC/Desktop/oit/lab2/lab%202u2/03_Circuito3_Sensor_DHT22_Multiplexado/diagram.json)
