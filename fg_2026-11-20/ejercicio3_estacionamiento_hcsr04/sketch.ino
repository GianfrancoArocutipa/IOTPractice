/*
 * ============================================================================
 * EXAMEN DE UNIDAD 2 - INTERNET DE LAS COSAS (UPT - 2026)
 * EJERCICIO 3: Sensor de Estacionamiento con HC-SR04 y 3 Displays de 7 Segmentos
 * Autores: Perez Peralta Fabrizio & Arocutipa Arocutipa Gian Franco
 * ============================================================================
 * Funcionamiento:
 *   - Mide distancia con sensor ultrasonico HC-SR04 en el rango 0 a 330 cm.
 *   - Muestra la distancia exacta en centimetros en 3 displays de 7 segmentos
 *     (Catodo Comun) multiplexados por Persistencia de la Vision (POV).
 *   - Indicadores visuales y sonoros segun distancia:
 *       * Distancia > 300 cm (> 3.0 m)     -> LED VERDE parpadeando.
 *       * Distancia 100 a 300 cm (1 a 3 m) -> LED NARANJA encendido fijo.
 *       * Distancia < 100 cm (< 1.0 m)     -> LED ROJO encendido + ALARMA SONORA.
 * ============================================================================
 */

// ==================== DEFINICION DE PINES ====================
// 7 segmentos compartidos (A, B, C, D, E, F, G) con resistencias de 560 Ohm
const int PINES_SEG[7] = {2, 3, 4, 5, 6, 7, 8};

// Seleccion de digito (Catodo Comun: LOW = digito activo, HIGH = digito apagado)
const int PIN_DIG_CENTENAS = 9;     // Display 1 (Izquierda)
const int PIN_DIG_DECENAS  = 10;    // Display 2 (Centro)
const int PIN_DIG_UNIDADES = 11;    // Display 3 (Derecha)
const int PINES_DIG[3] = {PIN_DIG_CENTENAS, PIN_DIG_DECENAS, PIN_DIG_UNIDADES};

// Sensor Ultrasonico HC-SR04
const int PIN_TRIG = 12;
const int PIN_ECHO = 13;

// LEDs de señalizacion y Alarma Sonora (usando pines analogicos como salidas digitales)
const int PIN_LED_VERDE   = A0;     // > 3.0 m (> 300 cm) -> parpadeando
const int PIN_LED_NARANJA = A1;     // 1.0 m a 3.0 m (100..300 cm) -> fijo
const int PIN_LED_ROJO    = A2;     // < 1.0 m (< 100 cm) -> fijo
const int PIN_BUZZER      = A3;     // Alarma sonora cuando distancia < 100 cm

// ==================== TABLA DE DIGITOS (0 al 9) - CATODO COMUN ====================
// Orden de bits: {A, B, C, D, E, F, G}  (1 = encendido, 0 = apagado)
const byte TABLA_DIGITOS[10][7] = {
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

// ==================== PARAMETROS Y TEMPORIZADORES ====================
const int DIST_MAX_CM = 330;               // Rango maximo mostrado (0 - 330 cm)
const int UMBRAL_VERDE_CM = 300;           // > 300 cm (3.0 m)
const int UMBRAL_ROJO_CM  = 100;           // < 100 cm (1.0 m)
const int FREQ_ALARMA     = 1200;          // Frecuencia de alarma sonora (1200 Hz)

const unsigned long INTERVALO_SENSOR_MS   = 150;  // Medicion cada 150 ms (sin parpadeo en displays)
const unsigned long INTERVALO_MUX_MS      = 4;    // Cambio de digito cada 4 ms (~83 Hz por digito)
const unsigned long INTERVALO_PARPADEO_MS = 300;  // Parpadeo del LED verde cada 300 ms

// Variables de estado
int distanciaCm = 0;
int digitos[3]  = {0, 0, 0};               // [0]=centenas, [1]=decenas, [2]=unidades
int digitoActual = 0;
bool estadoLedVerde = false;

unsigned long ultimoSensorMs   = 0;
unsigned long ultimoMuxMs      = 0;
unsigned long ultimoParpadeoMs = 0;

// ==================== FUNCIONES DE MULTIPLEXACION (7 SEGMENTOS) ====================
void apagarTodosLosDigitos() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(PINES_DIG[i], HIGH); // Catodo comun en HIGH = digito apagado
  }
}

void escribirSegmentos(int numero) {
  if (numero < 0 || numero > 9) return;
  for (int s = 0; s < 7; s++) {
    digitalWrite(PINES_SEG[s], TABLA_DIGITOS[numero][s] ? HIGH : LOW);
  }
}

void actualizarMultiplexacion() {
  unsigned long ahora = millis();
  if (ahora - ultimoMuxMs >= INTERVALO_MUX_MS) {
    ultimoMuxMs = ahora;

    // 1. Apagar todos los digitos antes de cambiar segmentos (evita efecto fantasma)
    apagarTodosLosDigitos();

    // 2. Cargar los segmentos del digito actual
    escribirSegmentos(digitos[digitoActual]);

    // 3. Activar unicamente el catodo del digito actual (LOW)
    digitalWrite(PINES_DIG[digitoActual], LOW);

    // 4. Avanzar al siguiente digito (0 -> 1 -> 2 -> 0)
    digitoActual = (digitoActual + 1) % 3;
  }
}

// ==================== FUNCION DE MEDICION CON HC-SR04 ====================
int medirDistanciaCm() {
  // Apagar displays brevemente durante el pulso ultrasonico para maxima estabilidad
  apagarTodosLosDigitos();

  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  // Timeout de 23000 us cubre hasta ~394 cm (suficiente para 330 cm)
  unsigned long duracionUs = pulseIn(PIN_ECHO, HIGH, 23000UL);

  if (duracionUs == 0) {
    return DIST_MAX_CM; // Fuera de rango -> mostrar tope 330 cm
  }

  int dist = (int)((duracionUs * 0.0343) / 2.0 + 0.5);

  // Limitar estrictamente al rango 0 - 330 cm
  if (dist < 0) dist = 0;
  if (dist > DIST_MAX_CM) dist = DIST_MAX_CM;

  return dist;
}

// ==================== ACTUALIZACION DE LEDs Y ALARMA ====================
void actualizarIndicadores() {
  unsigned long ahora = millis();

  if (distanciaCm > UMBRAL_VERDE_CM) {
    // ZONA SEGURA (> 3.0 m): LED verde parpadeando
    if (ahora - ultimoParpadeoMs >= INTERVALO_PARPADEO_MS) {
      ultimoParpadeoMs = ahora;
      estadoLedVerde = !estadoLedVerde;
    }
    digitalWrite(PIN_LED_VERDE,   estadoLedVerde ? HIGH : LOW);
    digitalWrite(PIN_LED_NARANJA, LOW);
    digitalWrite(PIN_LED_ROJO,    LOW);
    noTone(PIN_BUZZER);
  } else if (distanciaCm >= UMBRAL_ROJO_CM) {
    // ZONA DE PRECAUCION (1.0 m a 3.0 m): LED naranja fijo
    estadoLedVerde = false;
    digitalWrite(PIN_LED_VERDE,   LOW);
    digitalWrite(PIN_LED_NARANJA, HIGH);
    digitalWrite(PIN_LED_ROJO,    LOW);
    noTone(PIN_BUZZER);
  } else {
    // ZONA DE PELIGRO (< 1.0 m): LED rojo fijo + Alarma sonora
    estadoLedVerde = false;
    digitalWrite(PIN_LED_VERDE,   LOW);
    digitalWrite(PIN_LED_NARANJA, LOW);
    digitalWrite(PIN_LED_ROJO,    HIGH);
    tone(PIN_BUZZER, FREQ_ALARMA);
  }
}

// ==================== CONFIGURACION INICIAL ====================
void setup() {
  Serial.begin(9600);

  // Configurar pines de segmentos A-G como salidas
  for (int s = 0; s < 7; s++) {
    pinMode(PINES_SEG[s], OUTPUT);
    digitalWrite(PINES_SEG[s], LOW);
  }

  // Configurar pines de control de digitos (apagados = HIGH)
  for (int d = 0; d < 3; d++) {
    pinMode(PINES_DIG[d], OUTPUT);
    digitalWrite(PINES_DIG[d], HIGH);
  }

  // Configurar HC-SR04
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  // Configurar LEDs y Buzzer
  pinMode(PIN_LED_VERDE,   OUTPUT);
  pinMode(PIN_LED_NARANJA, OUTPUT);
  pinMode(PIN_LED_ROJO,    OUTPUT);
  pinMode(PIN_BUZZER,      OUTPUT);

  digitalWrite(PIN_LED_VERDE,   LOW);
  digitalWrite(PIN_LED_NARANJA, LOW);
  digitalWrite(PIN_LED_ROJO,    LOW);
  noTone(PIN_BUZZER);

  Serial.println("=== SENSOR DE ESTACIONAMIENTO HC-SR04 (0 - 330 cm) ===");
}

// ==================== BUCLE PRINCIPAL ====================
void loop() {
  unsigned long ahora = millis();

  // 1. Medir distancia periodicamente sin bloquear la multiplexacion
  if (ahora - ultimoSensorMs >= INTERVALO_SENSOR_MS) {
    ultimoSensorMs = ahora;
    distanciaCm = medirDistanciaCm();

    // Descomponer distancia en Centenas, Decenas y Unidades
    digitos[0] = (distanciaCm / 100) % 10;
    digitos[1] = (distanciaCm / 10) % 10;
    digitos[2] = distanciaCm % 10;

    // Reporte por Monitor Serie
    Serial.print("Distancia: ");
    Serial.print(distanciaCm);
    Serial.print(" cm | Zona: ");
    if (distanciaCm > UMBRAL_VERDE_CM) {
      Serial.println("SEGURA (>3.0m) - LED Verde parpadeando");
    } else if (distanciaCm >= UMBRAL_ROJO_CM) {
      Serial.println("PRECAUCION (1.0m-3.0m) - LED Naranja");
    } else {
      Serial.println("PELIGRO (<1.0m) - LED Rojo + ALARMA");
    }
  }

  // 2. Actualizar LEDs y Buzzer de forma no bloqueante
  actualizarIndicadores();

  // 3. Refrescar los 3 displays de 7 segmentos continuamente
  actualizarMultiplexacion();
}
