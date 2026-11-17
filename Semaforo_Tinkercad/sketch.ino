// PROYECTO: SEMÁFORO INTELIGENTE CON TEMPORIZADOR EN DISPLAY DE 7 SEGMENTOS
// Compatible con Tinkercad Circuits y Wokwi
// Basado en el diseño extraído de Semaforo.brd

// ==================== PINES DE LOS LEDS DEL SEMÁFORO ====================
const int LED_ROJO     = 7;   // D7 en Arduino Uno
const int LED_AMARILLO = 8;   // D8 en Arduino Uno
const int LED_VERDE    = 10;  // D10 en Arduino Uno

// ==================== PINES DEL DISPLAY DE 7 SEGMENTOS ====================
// Mapeo exacto extraído de Semaforo.brd:
const int SEG_A = 13;  // D13 -> Segmento A (Pin 7 del display)
const int SEG_B = 12;  // D12 -> Segmento B (Pin 6 del display)
const int SEG_C = 11;  // D11 -> Segmento C (Pin 4 del display)
const int SEG_D = 9;   // D9  -> Segmento D (Pin 2 del display)
const int SEG_E = 6;   // D6  -> Segmento E (Pin 1 del display)
const int SEG_F = 5;   // D5  -> Segmento F (Pin 9 del display)
const int SEG_G = 4;   // D4  -> Segmento G (Pin 10 del display)

// Tabla de segmentos para Cátodo Común (1 = Encendido, 0 = Apagado)
// Segmentos: {A, B, C, D, E, F, G}
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
  // Configuración de pines de los LEDs
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  // Configuración de pines del Display
  pinMode(SEG_A, OUTPUT);
  pinMode(SEG_B, OUTPUT);
  pinMode(SEG_C, OUTPUT);
  pinMode(SEG_D, OUTPUT);
  pinMode(SEG_E, OUTPUT);
  pinMode(SEG_F, OUTPUT);
  pinMode(SEG_G, OUTPUT);

  apagarLeds();
  apagarDisplay();
}

// Función para mostrar un dígito en el display de 7 segmentos
void mostrarNumero(int num) {
  if (num < 0 || num > 9) return;
  digitalWrite(SEG_A, numeros[num][0]);
  digitalWrite(SEG_B, numeros[num][1]);
  digitalWrite(SEG_C, numeros[num][2]);
  digitalWrite(SEG_D, numeros[num][3]);
  digitalWrite(SEG_E, numeros[num][4]);
  digitalWrite(SEG_F, numeros[num][5]);
  digitalWrite(SEG_G, numeros[num][6]);
}

// Función para apagar todos los segmentos del display
void apagarDisplay() {
  digitalWrite(SEG_A, LOW);
  digitalWrite(SEG_B, LOW);
  digitalWrite(SEG_C, LOW);
  digitalWrite(SEG_D, LOW);
  digitalWrite(SEG_E, LOW);
  digitalWrite(SEG_F, LOW);
  digitalWrite(SEG_G, LOW);
}

// Función para apagar los 3 LEDs del semáforo
void apagarLeds() {
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);
}

void loop() {
  // ================= 1. FASE VERDE (Paso vehicular) =================
  apagarLeds();
  digitalWrite(LED_VERDE, HIGH);
  // Cuenta regresiva del 5 al 1
  for (int i = 5; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }

  // ================= 2. FASE AMARILLA (Precaución) =================
  apagarLeds();
  digitalWrite(LED_AMARILLO, HIGH);
  // Cuenta regresiva de 2 segundos (2 y 1)
  for (int i = 2; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }

  // ================= 3. FASE ROJA (Detención) =================
  apagarLeds();
  digitalWrite(LED_ROJO, HIGH);
  // Cuenta regresiva del 5 al 1
  for (int i = 5; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }
}
