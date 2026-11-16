# Laboratorio 2.5: ESP32 con ThingSpeak (Medición de Nivel de Agua)

**Universidad Privada de Tacna**  
**Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas (IoT)  
**Docente:** Mgr. Alex Juan Yanqui Constancio  
**Autores:** Perez Fabrizio - Arocutipa Gian Franco  
**Documento base:** [Lab 2.5 - Esp32 Thingspeak.pdf](file:///c:/Users/PC/Desktop/oit/Lab%202.5%20-%20Esp32%20Thingspeak.pdf) (Guía de Laboratorio Nº10)

---

## 📋 Resumen del Proyecto

Este laboratorio implementa un sistema inteligente de monitoreo de nivel y volumen para un **tanque de agua cilíndrico** de dimensiones industriales simulado en **Wokwi**:
- **Altura total del tanque:** $1.0\text{ m} = 100\text{ cm}$
- **Radio del tanque:** $0.5\text{ m} = 50\text{ cm}$
- **Capacidad máxima aproximada:** 
  $$\text{Volumen} = \pi \cdot r^2 \cdot h = \pi \cdot (50\text{ cm})^2 \cdot 100\text{ cm} \approx 785\,398\text{ cm}^3 \approx 785.4\text{ Litros}$$

### Características Operativas
1. **Medición de Distancia Ultrasónica:** Sensor **HC-SR04** colocado en la parte superior del tanque. Mide la distancia de vacío entre el sensor y la superficie del agua.
2. **Cálculo de Nivel y Volumen:**
   - $\text{Nivel de Agua} = \text{Altura Tanque} - \text{Distancia Vacío}$
   - $\text{Volumen (Litros)} = \frac{\pi \cdot r^2 \cdot \text{Nivel de Agua}}{1000}$
   - $\text{Porcentaje} = \left(\frac{\text{Nivel de Agua}}{\text{Altura Tanque}}\right) \times 100\%$
3. **Alarma de Emergencia (> 90% de capacidad):**
   - Cuando el volumen supera el **90%** ($> 706.8\text{ L}$ o nivel $> 90\text{ cm}$):
     - Se enciende el **LED rojo** de emergencia conectado al **GPIO 2**.
     - En la pantalla LCD 16x2 se muestra el aviso de alarma `!ALTA!`.
4. **Visualización Local en Pantalla LCD 16x2 I2C:**
   - Línea 0: `Vol: XXX.X L`
   - Línea 1: `Nivel: XX.X% !ALTA!`
5. **Telemetría en la Nube con MathWorks ThingSpeak:**
   - Conexión WiFi virtual Wokwi (`Wokwi-GUEST`).
   - Envío periódico cada **15 segundos** (cumpliendo la cuota gratuita de ThingSpeak).
   - **Canal ID:** `3440423`
   - **Write API Key:** `D67PP21TA1CXR5XI`
   - **Campo 1 (Field 1):** Volumen en Litros.
   - **Campo 2 (Field 2):** Porcentaje de llenado (%).

---

## 🔌 Tabla de Conexiones (Pinout Wokwi)

| Componente | Pin del Componente | Pin ESP32 (Wokwi ID) | Color de Cable | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **Sensor HC-SR04** | `VCC` | `esp:VIN` | Rojo | Alimentación 5V / VIN |
| | `TRIG` | `esp:D5` | Marrón | Disparo ultrasónico (GPIO 5) |
| | `ECHO` | `esp:D18` | Verde | Pulso de eco recibido (GPIO 18) |
| | `GND` | `esp:GND.1` | Negro | Tierra (Lado derecho) |
| **Pantalla LCD 16x2 (I2C)** | `GND` | `esp:GND.1` | Negro | Tierra común (Lado derecho) |
| | `VCC` | `esp:VIN` | Rojo | Alimentación 5V / VIN |
| | `SDA` | `esp:D21` | Púrpura | Línea de datos I2C (GPIO 21) |
| | `SCL` | `esp:D22` | Magenta | Línea de reloj I2C (GPIO 22) |
| **LED Rojo (Alarma)** | `Ánodo (A)` | `esp:D2` | Verde | Salida digital alarma (GPIO 2) |
| | `Cátodo (C)` | `r1:1` | Verde | Conexión a la resistencia |
| **Resistencia 220Ω** | `Pin 1` | `led:C` | Verde | Lado ánodo |
| | `Pin 2` | `esp:GND.2` | Negro | Retorno a tierra (Lado izquierdo) |

---

## 📦 Archivo de Librerías (`libraries.txt`)

Para que el simulador Wokwi compile correctamente, incluye estas dependencias en [libraries.txt](file:///c:/Users/PC/Desktop/oit/Lab2.5_ESP32_ThingSpeak/libraries.txt):

```text
LiquidCrystal I2C
ThingSpeak
```

---

## 📄 Archivo de Circuito (`diagram.json`)

El archivo [diagram.json](file:///c:/Users/PC/Desktop/oit/Lab2.5_ESP32_ThingSpeak/diagram.json) utiliza los identificadores de pines nativos de Wokwi (`esp:VIN`, `esp:D5`, `esp:D18`, `esp:D21`, `esp:D22`, `esp:D2`, `esp:GND.1`, `esp:GND.2`):

```json
{
  "version": 1,
  "author": "Perez Fabrizio - Arocutipa Gian Franco",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-esp32-devkit-v1",
      "id": "esp",
      "top": 0,
      "left": 0,
      "attrs": {}
    },
    {
      "type": "wokwi-hc-sr04",
      "id": "ultrasonic",
      "top": -140,
      "left": 120,
      "attrs": {
        "distance": "50"
      }
    },
    {
      "type": "wokwi-lcd1602",
      "id": "lcd",
      "top": 130,
      "left": 120,
      "attrs": {
        "pins": "i2c"
      }
    },
    {
      "type": "wokwi-led",
      "id": "led",
      "top": -70,
      "left": -100,
      "attrs": {
        "color": "red"
      }
    },
    {
      "type": "wokwi-resistor",
      "id": "r1",
      "top": 30,
      "left": -100,
      "attrs": {
        "value": "220"
      }
    }
  ],
  "connections": [
    [ "ultrasonic:VCC", "esp:VIN", "red", [ "v20", "h-180", "v160" ] ],
    [ "ultrasonic:TRIG", "esp:D5", "brown", [ "v30", "h-50", "v90" ] ],
    [ "ultrasonic:ECHO", "esp:D18", "green", [ "v40", "h-40", "v60" ] ],
    [ "ultrasonic:GND", "esp:GND.1", "black", [ "v50", "h-60", "v150" ] ],
    [ "lcd:GND", "esp:GND.1", "black", [ "h-30", "v-40", "h-20" ] ],
    [ "lcd:VCC", "esp:VIN", "red", [ "h-40", "v60", "h-180", "v-150" ] ],
    [ "lcd:SDA", "esp:D21", "purple", [ "h-20", "v-120" ] ],
    [ "lcd:SCL", "esp:D22", "magenta", [ "h-10", "v-160" ] ],
    [ "esp:D2", "led:A", "green", [ "h20", "v80", "h-200", "v-180" ] ],
    [ "led:C", "r1:1", "green", [ "v10" ] ],
    [ "r1:2", "esp:GND.2", "black", [ "v20", "h50", "v-50" ] ]
  ],
  "serialMonitor": {
    "display": "auto"
  },
  "dependencies": {}
}
```

---

## 💻 Código Fuente de Arduino (`sketch.ino`)

El código [sketch.ino](file:///c:/Users/PC/Desktop/oit/Lab2.5_ESP32_ThingSpeak/sketch.ino) integra la lógica del sensor ultrasónico, cálculo de volumen cilíndrico, control de display LCD, encendido de alarma por hardware y conexión de telemetría hacia ThingSpeak con control de reconexión WiFi:

```cpp
/*
 * Guía de Laboratorio Nº10 / Lab 2.5: "PLACA ESP32 CON THINGSPEAK"
 * Medición de Nivel de Agua en Tanque Cilíndrico y Telemetría IoT
 * Universidad Privada de Tacna - Escuela de Ingeniería de Sistemas
 * Docente: Mgr. Alex Juan Yanqui Constancio
 * Autores: Perez Fabrizio - Arocutipa Gian Franco
 */

#include <Wire.h> 
#include <LiquidCrystal_I2C.h> 
#include <WiFi.h> 
#include <ThingSpeak.h> 
 
// ==================== CONFIGURACIÓN WIFI ====================
const char* WIFI_SSID = "Wokwi-GUEST";   
const char* WIFI_PASS = "";    
 
// ================= CONFIGURACIÓN THINGSPEAK =================
// Credenciales oficiales de la guía de laboratorio
unsigned long CHANNEL_ID = 3440423;              
const char* WRITE_API_KEY = "D67PP21TA1CXR5XI"; 
 
// ================== CONFIGURACIÓN DE PINES ==================
const int PIN_TRIG = 5;       // Trigger HC-SR04
const int PIN_ECHO = 18;      // Echo HC-SR04
const int PIN_LED  = 2;       // LED indicador de alarma (> 90%)
 
// ============== CONFIGURACIÓN TANQUE CILÍNDRICO ==============
// Tanque: 1 metro de alto (100 cm), 0.5 metros de radio (50 cm)
const float ALTURA_TANQUE = 100.0;  // cm
const float RADIO_TANQUE  = 50.0;   // cm
const float PI_CONST      = 3.14159265; 
 
// ================= INICIALIZACIÓN DE OBJETOS =================
// Pantalla LCD 16x2 vía I2C (Dirección estándar 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2);  
WiFiClient client; 
 
// Temporizador de envío a ThingSpeak (Mínimo 15s para plan gratuito)
unsigned long ultimoEnvio = 0; 
const unsigned long INTERVALO_ENVIO = 15000; // 15 segundos 
 
void setup() { 
  Serial.begin(115200); 
  Serial.println("\n--- INICIANDO SISTEMA DE MEDICION DE NIVEL ---"); 
 
  pinMode(PIN_TRIG, OUTPUT); 
  pinMode(PIN_ECHO, INPUT); 
  pinMode(PIN_LED, OUTPUT); 
 
  // Inicialización de la pantalla LCD
  lcd.init(); 
  lcd.backlight(); 
   
  // Conexión WiFi en Wokwi
  lcd.setCursor(0, 0); 
  lcd.print("Conectando WiFi"); 
  WiFi.begin(WIFI_SSID, WIFI_PASS); 
   
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500); 
    Serial.print("."); 
  } 
   
  Serial.println("\nWiFi Conectado!"); 
  lcd.clear(); 
  lcd.print("WiFi Conectado"); 
  delay(1500); 
  lcd.clear(); 
 
  // Inicialización del cliente ThingSpeak
  ThingSpeak.begin(client); 
} 
 
void loop() { 
  // --- 1. MEDICIÓN DE DISTANCIA CON HC-SR04 --- 
  digitalWrite(PIN_TRIG, LOW); 
  delayMicroseconds(2); 
  digitalWrite(PIN_TRIG, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(PIN_TRIG, LOW); 
 
  long duracion = pulseIn(PIN_ECHO, HIGH); 
  // Velocidad del sonido = 0.0343 cm/us (ida y vuelta / 2)
  float distancia_vacio = duracion * 0.0343 / 2.0; 
 
  // --- 2. CÁLCULO DE NIVEL Y VOLUMEN --- 
  float nivel_agua = ALTURA_TANQUE - distancia_vacio;  
   
  // Limitación para evitar lecturas falsas por rebotes acústicos
  if (nivel_agua < 0) nivel_agua = 0; 
  if (nivel_agua > ALTURA_TANQUE) nivel_agua = ALTURA_TANQUE; 
 
  // Volumen Cilindro: V = pi * r^2 * h (en cm3). 1 L = 1000 cm3
  float volumen_cm3 = PI_CONST * (RADIO_TANQUE * RADIO_TANQUE) * nivel_agua; 
  float volumen_litros = volumen_cm3 / 1000.0; 
  float porcentaje = (nivel_agua / ALTURA_TANQUE) * 100.0; 
 
  // --- 3. CONTROL DE ALARMA (> 90%) --- 
  if (porcentaje > 90.0) { 
    digitalWrite(PIN_LED, HIGH); 
  } else { 
    digitalWrite(PIN_LED, LOW); 
  } 
 
  // --- 4. VISUALIZACIÓN EN LCD 16X2 --- 
  lcd.setCursor(0, 0); 
  lcd.print("Vol: "); 
  lcd.print(volumen_litros, 1); 
  lcd.print(" L       "); // Espacios para limpiar dígitos sobrantes
 
  lcd.setCursor(0, 1); 
  lcd.print("Nivel: "); 
  lcd.print(porcentaje, 1); 
  lcd.print("% "); 
  if (porcentaje > 90.0) { 
    lcd.print("!ALTA!"); 
  } else { 
    lcd.print("      "); 
  } 
 
  // --- 5. MONITOREO SERIAL LOCAL ---
  Serial.print("Dist. Vacio: "); Serial.print(distancia_vacio, 1);
  Serial.print(" cm | Nivel: "); Serial.print(nivel_agua, 1);
  Serial.print(" cm | Vol: "); Serial.print(volumen_litros, 1);
  Serial.print(" L | Porc: "); Serial.print(porcentaje, 1);
  Serial.println("%");
 
  // --- 6. ENVÍO DE TELEMETRÍA A THINGSPEAK (CADA 15s) --- 
  if (millis() - ultimoEnvio >= INTERVALO_ENVIO) { 
    if (WiFi.status() != WL_CONNECTED) { 
      Serial.println("Reconectando a WiFi..."); 
      WiFi.disconnect(); 
      WiFi.reconnect(); 
    } else { 
      // Configuración de los canales de ThingSpeak
      ThingSpeak.setField(1, volumen_litros); // Campo 1: Volumen en Litros 
      ThingSpeak.setField(2, porcentaje);     // Campo 2: Porcentaje de llenado 
 
      // Transmisión HTTP a los servidores de ThingSpeak
      int respuesta = ThingSpeak.writeFields(CHANNEL_ID, WRITE_API_KEY); 
 
      if (respuesta == 200) { 
        Serial.println(">> [ThingSpeak] ¡Datos enviados correctamente! (HTTP 200)"); 
      } else { 
        Serial.print(">> [ThingSpeak] Error en envío. Código HTTP: "); 
        Serial.println(respuesta); 
      } 
    } 
    ultimoEnvio = millis(); 
  } 
 
  delay(200); // Frecuencia de actualización en pantalla local
}
```

---

## ⚙️ Configuración en la Plataforma ThingSpeak

1. Iniciar sesión en [ThingSpeak MathWorks](https://thingspeak.mathworks.com/).
2. Ir a **Channels** $\rightarrow$ **My Channels** $\rightarrow$ **New Channel**:
   - **Name:** `Nivel de Tanque`
   - **Field 1:** `Volumen` (guardará litros)
   - **Field 2:** `Porcentaje` (guardará porcentaje de $0$ a $100\%$)
3. Guardar el canal y abrir la pestaña **API Keys**:
   - Copiar la **Write API Key** y el **Channel ID** si se desea utilizar un canal propio.
   - En este proyecto ya vienen configuradas las credenciales del laboratorio:
     - `CHANNEL_ID = 3440423`
     - `WRITE_API_KEY = "D67PP21TA1CXR5XI"`
4. En **Private View**, se observarán las 2 gráficas dinámicas actualizándose cada 15 segundos al mover el deslizador de distancia del sensor en Wokwi.

---

## 📝 Resolución del Cuestionario (Página 12)

> **Pregunta 1:** *Modifique el programa, adicione un control de válvula de desagüe (servomotor), que se pueda con control manual y también con control web.*

### Solución Técnica
1. **Hardware Adicional en Wokwi:**
   - Servomotor SG90 (`wokwi-servo`) conectado al pin **GPIO 13** del ESP32.
   - Pulsador físico (`wokwi-pushbutton`) conectado al pin **GPIO 4** con resistencia pull-up interna (`INPUT_PULLUP`).
2. **Lógica de Control Dual:**
   - **Control Manual (Local):** Al presionar el botón físico en GPIO 4, se conmuta el estado de la válvula ($0^\circ$ cerrada, $90^\circ$ abierta para desagüe).
   - **Control Web (Remoto):** Se lee el **Campo 3 (Field 3)** del canal de ThingSpeak usando `ThingSpeak.readIntField(CHANNEL_ID, 3, READ_API_KEY)`. Si el valor web es `1`, la válvula se abre; si es `0`, la válvula se cierra.
   - **Seguridad Automática:** Si el nivel supera el $95\%$, la válvula se abre automáticamente para evitar desborde del tanque.
