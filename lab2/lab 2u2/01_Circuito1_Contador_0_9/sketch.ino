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