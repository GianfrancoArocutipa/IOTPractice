// Pines de los 7 segmentos compartidos (A, B, C, D, E, F, G)
const int pinesSegmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de los catodos comunes de los 3 displays (Centenas, Decenas, Unidades)
const int pinesDigitos[3] = {9, 10, 11};

// Pines del sensor HC-SR04
const int pinTrig = 12;
const int pinEcho = 13;

// Pines de los LEDs y alarma sonora
const int ledVerde   = A0;
const int ledNaranja = A1;
const int ledRojo    = A2;
const int pinBuzzer  = A3;

// Tabla de digitos 0 a 9 para display de catodo comun (A, B, C, D, E, F, G)
const byte tablaDigitos[10][7] = {
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

int distanciaCm = 0;
int digitos[3]  = {0, 0, 0};
int digitoActual = 0;
bool estadoVerde = false;

unsigned long tiempoSensor   = 0;
unsigned long tiempoMux      = 0;
unsigned long tiempoParpadeo = 0;

void apagarDigitos() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(pinesDigitos[i], HIGH);
  }
}

int medirDistanciaCm() {
  apagarDigitos();
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  unsigned long duracion = pulseIn(pinEcho, HIGH, 23000);
  if (duracion == 0) {
    return 330;
  }
  int cm = (int)((duracion * 0.0343) / 2.0 + 0.5);
  return constrain(cm, 0, 330);
}

void refrescarDisplays() {
  apagarDigitos();
  int numero = digitos[digitoActual];
  for (int s = 0; s < 7; s++) {
    digitalWrite(pinesSegmentos[s], tablaDigitos[numero][s]);
  }
  digitalWrite(pinesDigitos[digitoActual], LOW);
  digitoActual = (digitoActual + 1) % 3;
}

void setup() {
  for (int s = 0; s < 7; s++) {
    pinMode(pinesSegmentos[s], OUTPUT);
  }
  for (int d = 0; d < 3; d++) {
    pinMode(pinesDigitos[d], OUTPUT);
    digitalWrite(pinesDigitos[d], HIGH);
  }

  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledNaranja, OUTPUT);
  pinMode(ledRojo, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);
}

void loop() {
  unsigned long ahora = millis();

  // Medir distancia cada 150 ms y separar en 3 digitos (0 - 330 cm)
  if (ahora - tiempoSensor >= 150) {
    tiempoSensor = ahora;
    distanciaCm = medirDistanciaCm();
    digitos[0] = (distanciaCm / 100) % 10;
    digitos[1] = (distanciaCm / 10) % 10;
    digitos[2] = distanciaCm % 10;
  }

  // Controlar LEDs y alarma segun la distancia
  if (distanciaCm > 300) {
    // Mayor a 3.0 m: LED verde parpadeando
    if (ahora - tiempoParpadeo >= 300) {
      tiempoParpadeo = ahora;
      estadoVerde = !estadoVerde;
    }
    digitalWrite(ledVerde, estadoVerde);
    digitalWrite(ledNaranja, LOW);
    digitalWrite(ledRojo, LOW);
    noTone(pinBuzzer);
  } else if (distanciaCm >= 100) {
    // De 1.0 m hasta 3.0 m: LED naranja
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledNaranja, HIGH);
    digitalWrite(ledRojo, LOW);
    noTone(pinBuzzer);
  } else {
    // Menor a 1.0 m: LED rojo y alarma sonora
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledNaranja, LOW);
    digitalWrite(ledRojo, HIGH);
    tone(pinBuzzer, 1200);
  }

  // Multiplexar los 3 displays cada 4 ms
  if (ahora - tiempoMux >= 4) {
    tiempoMux = ahora;
    refrescarDisplays();
  }
}
