/*
 * ============================================================================
 * EXAMEN DE UNIDAD 2 - INTERNET DE LAS COSAS (UPT - 2026)
 * EJERCICIO 2: Monitor de Temperatura de Precision (10 C a 40 C) en Modo Punto
 * Autores: Perez Peralta Fabrizio & Arocutipa Arocutipa Gian Franco
 * ============================================================================
 * Funcionamiento:
 *   - Lee la temperatura ambiente usando el sensor analogico TMP36 en A0.
 *   - Rango monitoreado: 10 C (LED 1) hasta 40 C (LED 10).
 *   - MODO PUNTO: Solo permanece encendido el LED del intervalo actual.
 *   - Si la temperatura llega al LED 10 (~40 C):
 *       1) Se enclava (activa y memoriza) una alarma sonora en el Buzzer.
 *       2) El display de 7 segmentos se enciende mostrando la letra "E" (Error).
 *       3) La alarma y la "E" permanecen activas AUNQUE la temperatura baje.
 *   - Al presionar el pulsador de reinicio (RESET), se apaga la alarma y el
 *     display (siempre que la temperatura ya haya bajado del nivel critico).
 * ============================================================================
 */

// ==================== DEFINICION DE PINES ====================
const int PIN_TMP36  = A0;          // Salida analogica Vout del sensor TMP36
const int PIN_RESET  = 12;          // Pulsador de reinicio (conectado a GND, usa INPUT_PULLUP)
const int PIN_BUZZER = 13;          // Buzzer piezoelectrico de alarma sonora

// 10 LEDs ordenados del LED 1 (10 C) al LED 10 (40 C)
const int NUM_LEDS = 10;
const int PINES_LEDS[NUM_LEDS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

// Display de 7 segmentos (Catodo Comun) - Segmentos que forman la letra "E"
// Letra "E" = segmentos A, D, E, F, G encendidos (B y C siempre apagados)
const int SEG_A = A1;
const int SEG_D = A2;
const int SEG_E = A3;
const int SEG_F = A4;
const int SEG_G = A5;

// ==================== CONSTANTES DE RANGO DE TEMPERATURA ====================
const float TEMP_MIN = 10.0;        // LED 1 indica 10 C
const float TEMP_MAX = 40.0;        // LED 10 indica 40 C
const int   FREQ_ALARMA = 1000;     // Frecuencia de la alarma sonora (1000 Hz)

// ==================== VARIABLES DE ESTADO ====================
bool alarmaActiva = false;          // Memoria (enclavamiento) de la alarma
unsigned long ultimoReporteMs = 0;  // Temporizador no bloqueante para Monitor Serie

// ==================== CONTROL DEL DISPLAY DE 7 SEGMENTOS ====================
void mostrarErrorDisplay(bool encender) {
  int estado = encender ? HIGH : LOW;
  digitalWrite(SEG_A, estado);
  digitalWrite(SEG_D, estado);
  digitalWrite(SEG_E, estado);
  digitalWrite(SEG_F, estado);
  digitalWrite(SEG_G, estado);
}

// ==================== CONTROL DE LOS 10 LEDs (MODO PUNTO) ====================
void encenderSoloLed(int indice) {
  // Apaga todos los LEDs excepto el que coincide con "indice" (0..9)
  // Si indice == -1 (fuera de rango inferior), todos quedan apagados
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(PINES_LEDS[i], (i == indice) ? HIGH : LOW);
  }
}

// ==================== LECTURA PROMEDIADA DEL SENSOR TMP36 ====================
float leerTemperaturaTMP36() {
  // Promediar 10 muestras para estabilizar la lectura del ADC
  long sumaADC = 0;
  for (int i = 0; i < 10; i++) {
    sumaADC += analogRead(PIN_TMP36);
    delay(2);
  }
  float promedioADC = sumaADC / 10.0;

  // Convertir lectura ADC (0..1023) a voltaje (0..5V)
  float voltaje = promedioADC * (5.0 / 1024.0);

  // Formula oficial del TMP36: 500 mV de offset a 0 C y 10 mV por cada grado C
  float tempC = (voltaje - 0.5) * 100.0;
  return tempC;
}

// ==================== CONFIGURACION INICIAL ====================
void setup() {
  Serial.begin(9600);

  // Configurar los 10 LEDs como salidas e iniciarlos apagados
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(PINES_LEDS[i], OUTPUT);
    digitalWrite(PINES_LEDS[i], LOW);
  }

  // Configurar pines del display de 7 segmentos como salidas e iniciarlo apagado
  pinMode(SEG_A, OUTPUT);
  pinMode(SEG_D, OUTPUT);
  pinMode(SEG_E, OUTPUT);
  pinMode(SEG_F, OUTPUT);
  pinMode(SEG_G, OUTPUT);
  mostrarErrorDisplay(false);

  // Configurar pulsador con resistencia pull-up interna (LOW = presionado)
  pinMode(PIN_RESET, INPUT_PULLUP);

  // Configurar buzzer como salida
  pinMode(PIN_BUZZER, OUTPUT);
  noTone(PIN_BUZZER);

  Serial.println("=== MONITOR DE TEMPERATURA DE PRECISION (10 C - 40 C) ===");
  Serial.println("Modo Punto: LED 1 = 10 C ... LED 10 = 40 C (Activa Alarma + E)");
}

// ==================== BUCLE PRINCIPAL ====================
void loop() {
  // 1. Leer temperatura actual del sensor TMP36
  float tempC = leerTemperaturaTMP36();

  // 2. Determinar el indice de LED (0 a 9) en modo punto
  //    Se usa redondeo lineal sobre [10 C, 40 C] -> [0, 9] (pasos de 3.33 C)
  //    Con tolerancia de 0.5 C en 10 C para compensar cuantizacion del ADC (~0.49 C)
  int ledActual = -1;
  if (tempC >= (TEMP_MIN - 0.5)) {
    float posicion = (tempC - TEMP_MIN) * 9.0 / (TEMP_MAX - TEMP_MIN);
    ledActual = (int)round(posicion);
    if (ledActual < 0) ledActual = 0;
    if (ledActual > 9) ledActual = 9;
  }

  // 3. Actualizar la fila de LEDs en MODO PUNTO (un unico LED encendido)
  encenderSoloLed(ledActual);

  // 4. Evaluar disparo de alarma (si llega al LED 10 -> indice 9)
  if (ledActual == 9) {
    alarmaActiva = true;
  }

  // 5. Leer pulsador de reinicio (RESET) con antirebote no bloqueante
  //    Al estar con INPUT_PULLUP, presionado = LOW
  if (digitalRead(PIN_RESET) == LOW) {
    delay(30); // Antirebote breve
    if (digitalRead(PIN_RESET) == LOW) {
      if (ledActual < 9) {
        alarmaActiva = false;
        Serial.println(">>> [RESET] Alarma reiniciada por el usuario.");
      } else {
        Serial.println(">>> [AVISO] Baje la temperatura por debajo del LED 10 para reiniciar.");
      }
      // Esperar a que suelte el boton para evitar lecturas repetidas
      while (digitalRead(PIN_RESET) == LOW) {
        delay(10);
      }
    }
  }

  // 6. Aplicar estado de Alarma en Buzzer y Display de 7 segmentos ("E")
  if (alarmaActiva) {
    tone(PIN_BUZZER, FREQ_ALARMA);    // Alarma sonora continua
    mostrarErrorDisplay(true);        // Muestra la letra "E" en el display
  } else {
    noTone(PIN_BUZZER);               // Buzzer en silencio
    mostrarErrorDisplay(false);       // Display apagado
  }

  // 7. Mostrar diagnostico por Monitor Serie cada 400 ms
  if (millis() - ultimoReporteMs >= 400) {
    ultimoReporteMs = millis();
    Serial.print("Temp: ");
    Serial.print(tempC, 2);
    Serial.print(" C | LED activo: ");
    if (ledActual >= 0) {
      Serial.print("LED ");
      Serial.print(ledActual + 1);
    } else {
      Serial.print("Ninguno (<10 C)");
    }
    Serial.print(" | Alarma: ");
    Serial.print(alarmaActiva ? "ACTIVA [E]" : "Inactiva");
    Serial.println();
  }
}
