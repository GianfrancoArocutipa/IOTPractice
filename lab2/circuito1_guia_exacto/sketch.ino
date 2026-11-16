// CIRCUITO 1: CONTADOR DE 0 A 9 (GUÍA OFICIAL LAB 2.2 - PÁG. 6 Y 7)
// Control de Displays de 7 segmentos de cátodo común con Arduino Nano

// Declaramos los pines de salida, en el proyecto así lo tenemos cableado
int a = 2; 
int b = 3; 
int c = 4; 
int d = 5; 
int e = 6; 
int f = 7; 
int g = 8;  
int tiempo = 500; // Tiempo de espera entre números (ms)

// Configuramos los pines de los segmentos como salidas
void setup() { 
  pinMode(a, OUTPUT); 
  pinMode(b, OUTPUT); 
  pinMode(c, OUTPUT); 
  pinMode(d, OUTPUT); 
  pinMode(e, OUTPUT); 
  pinMode(f, OUTPUT); 
  pinMode(g, OUTPUT);
} 
 
void loop() { 
  // Cero (0)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 1); 
  digitalWrite(f, 1); 
  digitalWrite(g, 0); 
  delay(tiempo); 
 
  // Uno (1)
  digitalWrite(a, 0); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 0); 
  digitalWrite(e, 0); 
  digitalWrite(f, 0); 
  digitalWrite(g, 0); 
  delay(tiempo); 
 
  // Dos (2)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 0); 
  digitalWrite(d, 1); 
  digitalWrite(e, 1); 
  digitalWrite(f, 0); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Tres (3)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 0); 
  digitalWrite(f, 0); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Cuatro (4)
  digitalWrite(a, 0); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 0); 
  digitalWrite(e, 0); 
  digitalWrite(f, 1); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Cinco (5)
  digitalWrite(a, 1); 
  digitalWrite(b, 0); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 0); 
  digitalWrite(f, 1); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Seis (6)
  digitalWrite(a, 1); 
  digitalWrite(b, 0); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 1); 
  digitalWrite(f, 1); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Siete (7)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 0); 
  digitalWrite(e, 0); 
  digitalWrite(f, 0); 
  digitalWrite(g, 0); 
  delay(tiempo); 
 
  // Ocho (8)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 1); 
  digitalWrite(f, 1); 
  digitalWrite(g, 1); 
  delay(tiempo); 
 
  // Nueve (9)
  digitalWrite(a, 1); 
  digitalWrite(b, 1); 
  digitalWrite(c, 1); 
  digitalWrite(d, 1); 
  digitalWrite(e, 0); 
  digitalWrite(f, 1); 
  digitalWrite(g, 1); 
  delay(tiempo); 
}
