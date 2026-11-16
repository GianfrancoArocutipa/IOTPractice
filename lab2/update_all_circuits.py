import json
import build_circuits_json

c2_json = build_circuits_json.c2_json_str
c3_json = build_circuits_json.c3_json_str

# Circuito 1 sketch adapted for the dual-display / transistor setup
c1_sketch = '''// CIRCUITO 1: CONTADOR 0 A 9 EN 1 DISPLAY DE 7 SEGMENTOS
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
  // Configurar pines de segmentos a..g como salida
  pinMode(a, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(c, OUTPUT);
  pinMode(d, OUTPUT);
  pinMode(e, OUTPUT);
  pinMode(f, OUTPUT);
  pinMode(g, OUTPUT);

  // Configurar pines de control de los transistores
  pinMode(pinTransistorUnidades, OUTPUT);
  pinMode(pinTransistorDecenas, OUTPUT);

  // Activamos el transistor del display de unidades y apagamos el de decenas
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
'''

# Circuito 2 sketch (Multiplexing 00 to 99)
c2_sketch = '''// CIRCUITO 2: CONTADOR 00 A 99 MULTIPLEXADO - ARDUINO NANO
// Guía de Laboratorio 2.2 - Páginas 8, 9 y 10

const byte segmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de habilitación a la base de los transistores 2N2222
const byte display1 = 9;   // Decenas (Transistor 1 -> sevseg2, col 22)
const byte display2 = 10;  // Unidades (Transistor 2 -> sevseg1, col 28)

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
  for (int contador = 0; contador < 100; contador++) {
    unsigned long t = millis();
    // Multiplexar continuamente durante 1000 ms (1 segundo por cada número)
    while (millis() - t < 1000) {
      mostrar(contador);
    }
  }
}
'''

# Circuito 3 sketch (DHT22 Temperature & Humidity + 7-segment Multiplexed Display)
c3_sketch = '''// CIRCUITO 3: SENSOR DIGITAL DHT22 CON DISPLAY MULTIPLEXADO - ARDUINO NANO
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
'''

# Chip 2N2222 definition
chip_json = '''{
  "name": "2n2222",
  "author": "ALEX JUAN YANQUI CONSTANCIO",
  "pins": [
    "",
    "BASE",
    "EMI",
    "COL"
  ]
}
'''

chip_c = '''#include "wokwi-api.h"
#include <stdlib.h>

typedef struct {
  pin_t pin_base;
  pin_t pin_col;
  pin_t pin_emi;
} chip_state_t;

static void on_base_change(void *user_data, pin_t pin, uint32_t level) {
  chip_state_t *chip = (chip_state_t *)user_data;
  
  if (level == HIGH) {
    // Transistor NPN Conduciendo: Conecta el colector a GND digital
    pin_mode(chip->pin_col, OUTPUT);
    pin_write(chip->pin_col, LOW); 
  } else {
    // Transistor NPN en Corte: Colector en alta impedancia (circuito abierto)
    pin_mode(chip->pin_col, INPUT); 
  }
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_base = pin_init("BASE", INPUT);
  chip->pin_col = pin_init("COL", INPUT); // Inicia abierto
  chip->pin_emi = pin_init("EMI", INPUT);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = on_base_change,
    .user_data = chip,
  };
  pin_watch(chip->pin_base, &watch_config);
}
'''

libraries_txt = '''DHT sensor library
'''

# Write 04_Circuito3_Sensor_DHT22_Nano.txt
with open("c:/Users/PC/Desktop/oit/lab2/04_Circuito3_Sensor_DHT22_Nano.txt", "w", encoding="utf-8") as f:
    f.write(f'''================================================================================
CIRCUITO 3: SENSOR DIGITAL DHT22 CON DISPLAY MULTIPLEXADO - ARDUINO NANO
(Correspondiente a la Guía de Laboratorio 2.2 - Sección 2.3 "Implemente DHT22")
================================================================================

Este circuito utiliza exactamente tu diagrama de montaje físico (Arduino Nano,
protoboard, 7 resistencias de 220Ω, 2 transistores 2N2222 en pines 9 y 10, y los
dos displays de cátodo común) e incorpora el sensor digital DHT22 conectado al pin D11.

¿CÓMO FUNCIONA?
1. El sensor DHT22 mide la temperatura y humedad ambiental cada 1.5 segundos.
2. La temperatura en °C (por ejemplo, 24°C) se descompone en decenas ('2') y unidades ('4').
3. El microcontrolador multiplexa los 2 displays a ~125 Hz mediante los transistores 2N2222:
   - Pin D9 = HIGH -> Transistor 1 conduce -> Muestra las Decenas en el Display Izquierdo.
   - Pin D10 = HIGH -> Transistor 2 conduce -> Muestra las Unidades en el Display Derecho.
4. En el Monitor Serial se imprime periódicamente la temperatura y humedad exactas.

INSTRUCCIONES PASO A PASO PARA WOKWI:
1. Abre tu proyecto en https://wokwi.com
2. En la pestaña "sketch.ino": Borra todo y pega el código de abajo (ARCHIVO: sketch.ino).
3. En la pestaña "diagram.json": Borra todo y pega el JSON de abajo (ARCHIVO: diagram.json).
4. En la pestaña "libraries.txt" (o el administrador de librerías):
   Agrega la línea:
   DHT sensor library
5. Asegúrate de tener los 2 archivos del Custom Chip 2N2222 (creados con el botón "+" -> "New File..."):
   - Archivo: 2n2222.chip.json (pega el contenido de ARCHIVO: 2n2222.chip.json)
   - Archivo: 2n2222.chip.c    (pega el contenido de ARCHIVO: 2n2222.chip.c)
6. Presiona el botón verde de "Play":
   - Verás la temperatura (24°C) reflejada inmediatamente en los dos displays: un "2" a la izquierda y un "4" a la derecha.
   - Haz clic sobre el sensor DHT22 durante la simulación para deslizar la temperatura (ejemplo: sube a 35°C o baja a 18°C) y verás cómo el display se actualiza al instante.

--------------------------------------------------------------------------------
ARCHIVO: sketch.ino
--------------------------------------------------------------------------------
{c3_sketch}
--------------------------------------------------------------------------------
ARCHIVO: diagram.json
--------------------------------------------------------------------------------
{c3_json}

--------------------------------------------------------------------------------
ARCHIVO: libraries.txt
--------------------------------------------------------------------------------
{libraries_txt}
--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.json
--------------------------------------------------------------------------------
{chip_json}
--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.c
--------------------------------------------------------------------------------
{chip_c}
''')

# Write 03_Circuito2_Contador_00_99_Multiplexado_Nano.txt
with open("c:/Users/PC/Desktop/oit/lab2/03_Circuito2_Contador_00_99_Multiplexado_Nano.txt", "w", encoding="utf-8") as f:
    f.write(f'''================================================================================
CIRCUITO 2: CONTADOR 00 A 99 MULTIPLEXADO CON TRANSISTORES 2N2222 - ARDUINO NANO
(Correspondiente a la Guía de Laboratorio 2.2 - Sección 2.2)
================================================================================

EXPLICACIÓN CLAVE DE POR QUÉ NO FUNCIONABA Y CÓMO ESTÁ CORREGIDO:
En tu circuito físico tenías dos puentes de cable directos a GND:
  - Uno conectando GND a la columna 22 (cátodo del display izquierdo).
  - Uno conectando la columna 22 a la columna 28 (cátodo del display derecho).
Al estar ambos cátodos cortocircuitados directamente a GND de forma permanente, los
transistores 2N2222 no tenían ningún control de conmutación. Por lo tanto, cuando
el programa enviaba las decenas, se iluminaban los dos displays a la vez, y cuando
enviaba las unidades, volvían a iluminarse los dos displays a la vez, viéndose números
duplicados y superpuestos.

SOLUCIÓN:
En este "diagram.json" se retiraron esos dos puentes directos a GND. De esta forma,
el cátodo de cada display queda gobernado ÚNICAMENTE por su respectivo transistor:
  - Transistor 1 (Pin D9) controla el Display Izquierdo (Decenas).
  - Transistor 2 (Pin D10) controla el Display Derecho (Unidades).
¡Con esto el multiplexado funciona al 100% y cuenta de 00 a 99 sin ningún parpadeo!

INSTRUCCIONES PARA WOKWI:
1. En la pestaña "sketch.ino": Pega el código de abajo.
2. En la pestaña "diagram.json": Pega el JSON de abajo.
3. Asegúrate de crear los dos archivos del chip 2N2222 (botón "+"):
   - 2n2222.chip.json
   - 2n2222.chip.c
4. Presiona "Play" y verás el conteo limpio de 00 a 99.

--------------------------------------------------------------------------------
ARCHIVO: sketch.ino
--------------------------------------------------------------------------------
{c2_sketch}
--------------------------------------------------------------------------------
ARCHIVO: diagram.json
--------------------------------------------------------------------------------
{c2_json}

--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.json
--------------------------------------------------------------------------------
{chip_json}
--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.c
--------------------------------------------------------------------------------
{chip_c}
''')

# Write 02_Circuito1_Contador_0_9_Nano.txt
with open("c:/Users/PC/Desktop/oit/lab2/02_Circuito1_Contador_0_9_Nano.txt", "w", encoding="utf-8") as f:
    f.write(f'''================================================================================
CIRCUITO 1: CONTADOR 0 A 9 EN DISPLAY DE 7 SEGMENTOS - ARDUINO NANO
(Correspondiente a la Guía de Laboratorio 2.2 - Sección 2.1)
================================================================================

EXPLICACIÓN DE COMPATIBILIDAD CON TU MONTAJE:
En la guía original, el Circuito 1 utiliza un solo display con su cátodo conectado a GND.
Si utilizas el montaje de dos displays con transistores (Pines D9 y D10), el código
original de la guía no encendía ningún transistor, por lo que los displays quedaban apagados
(o si los puenteabas a tierra, se encendían ambos displays mostrando números repetidos "00", "11"...).

En este código adaptado a tu circuito:
- El Pin 10 se coloca en HIGH para habilitar el transistor del Display Derecho (Unidades).
- El Pin 9 se coloca en LOW para mantener apagado el Display Izquierdo.
- De esta manera, el conteo de 0 a 9 se muestra limpiamente en un solo display tal como pide la guía.

INSTRUCCIONES PARA WOKWI:
1. En la pestaña "sketch.ino": Pega el código de abajo.
2. En la pestaña "diagram.json": Pega el JSON de abajo (el mismo circuito funcional).
3. Presiona "Play" y verás el conteo de 0 a 9 en el display derecho.

--------------------------------------------------------------------------------
ARCHIVO: sketch.ino
--------------------------------------------------------------------------------
{c1_sketch}
--------------------------------------------------------------------------------
ARCHIVO: diagram.json
--------------------------------------------------------------------------------
{c2_json}

--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.json
--------------------------------------------------------------------------------
{chip_json}
--------------------------------------------------------------------------------
ARCHIVO: 2n2222.chip.c
--------------------------------------------------------------------------------
{chip_c}
''')

# Write master file TODOS_LOS_EJERCICIOS_WOKWI.txt
with open("c:/Users/PC/Desktop/oit/lab2/TODOS_LOS_EJERCICIOS_WOKWI.txt", "w", encoding="utf-8") as f:
    f.write(f'''================================================================================
GUÍA MAESTRA DE EJERCICIOS RESUELTOS - LABORATORIO 2.2 ARDUINO NANO WOKWI
Autor: Gian Franco Arocutipa Arocutipa
================================================================================

CONTENIDO:
1. CIRCUITO 1: Contador 0 a 9 en 1 display (adaptado a tu montaje con transistores)
2. CIRCUITO 2: Contador 00 a 99 multiplexado con transistores 2N2222
3. CIRCUITO 3: Sensor DHT22 con visualización de temperatura en displays multiplexados
4. ARCHIVOS DEL CUSTOM CHIP 2N2222 (Requeridos para Circuito 1, 2 y 3)

================================================================================
1. CIRCUITO 1: CONTADOR DE 0 A 9
================================================================================
-- sketch.ino --
{c1_sketch}

-- diagram.json --
{c2_json}

================================================================================
2. CIRCUITO 2: CONTADOR DE 00 A 99 MULTIPLEXADO
================================================================================
-- sketch.ino --
{c2_sketch}

-- diagram.json --
{c2_json}

================================================================================
3. CIRCUITO 3: SENSOR DIGITAL DHT22 CON DISPLAY MULTIPLEXADO
================================================================================
-- sketch.ino --
{c3_sketch}

-- diagram.json --
{c3_json}

-- libraries.txt --
{libraries_txt}

================================================================================
4. ARCHIVOS DEL CUSTOM CHIP 2N2222 (COMUNES PARA TODOS LOS CIRCUITOS)
================================================================================
En Wokwi, haz clic en el botón "+" (junto a las pestañas de código) y crea estos 2 archivos:

-- 2n2222.chip.json --
{chip_json}

-- 2n2222.chip.c --
{chip_c}
''')

print("All 4 text files successfully generated and synchronized!")
