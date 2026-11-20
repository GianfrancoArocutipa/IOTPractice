// Pines del sensor, pulsador y buzzer
const int pinTMP36  = A0;
const int pinReset  = 12;
const int pinBuzzer = 13;

// Pines de los 10 LEDs (LED 1 = 10 C ... LED 10 = 40 C)
const int pinesLeds[10] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

// Pines del display de 7 segmentos para formar la letra "E" (A, D, E, F, G)
const int segmentosE[5] = {A1, A2, A3, A4, A5};

bool alarmaActiva = false;

void mostrarLetraE(bool encender) {
  for (int i = 0; i < 5; i++) {
    digitalWrite(segmentosE[i], encender ? HIGH : LOW);
  }
}

void setup() {
  for (int i = 0; i < 10; i++) {
    pinMode(pinesLeds[i], OUTPUT);
  }
  for (int i = 0; i < 5; i++) {
    pinMode(segmentosE[i], OUTPUT);
  }

  pinMode(pinReset, INPUT_PULLUP);
  pinMode(pinBuzzer, OUTPUT);
  mostrarLetraE(false);
}

void loop() {
  // Leer temperatura del sensor TMP36
  float voltaje = analogRead(pinTMP36) * (5.0 / 1024.0);
  float temperatura = (voltaje - 0.5) * 100.0;

  // Calcular indice del LED correspondiente al rango 10 C - 40 C (modo punto)
  int ledActual = -1;
  if (temperatura >= 9.5) {
    ledActual = constrain((int)round((temperatura - 10.0) * 9.0 / 30.0), 0, 9);
  }

  // Encender unicamente el LED del intervalo actual
  for (int i = 0; i < 10; i++) {
    digitalWrite(pinesLeds[i], (i == ledActual) ? HIGH : LOW);
  }

  // Activar y mantener alarma al llegar al LED 10 (40 C)
  if (ledActual == 9) {
    alarmaActiva = true;
  }

  // Reiniciar alarma al presionar el pulsador de reset
  if (digitalRead(pinReset) == LOW) {
    delay(30);
    if (digitalRead(pinReset) == LOW && ledActual < 9) {
      alarmaActiva = false;
    }
  }

  // Controlar buzzer y display mostrando "E"
  if (alarmaActiva) {
    tone(pinBuzzer, 1000);
    mostrarLetraE(true);
  } else {
    noTone(pinBuzzer);
    mostrarLetraE(false);
  }

  delay(50);
}
