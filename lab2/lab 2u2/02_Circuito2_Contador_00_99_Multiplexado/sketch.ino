// CIRCUITO 2: CONTADOR 00 A 99 MULTIPLEXADO - ARDUINO NANO
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