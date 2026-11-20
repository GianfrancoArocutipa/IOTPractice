/*
 * ============================================================================
 * EXAMEN DE UNIDAD 2 - INTERNET DE LAS COSAS (UPT - 2026)
 * EJERCICIO 1: Medicion de Nivel y Volumen en Dos Tanques con Control de Valvula
 * Autores: Perez Peralta Fabrizio & Arocutipa Arocutipa Gian Franco
 * ============================================================================
 * Especificaciones de cada tanque cilindrico:
 *   - Altura (H) = 2.0 m (200 cm)
 *   - Radio  (R) = 0.5 m (50 cm)
 *   - Area base  = PI * R^2 = 0.785398 m^2
 *   - Volumen maximo por tanque = PI * R^2 * H = 1.5708 m^3 = 1570.80 Litros
 *
 * Logica de control:
 *   - Mide el nivel (h1 y h2) y calcula el volumen en litros de ambos tanques.
 *   - Visualiza en el LCD 16x2 el volumen (L), porcentaje (%) y estado.
 *   - Si el nivel alcanza >= 90% del volumen total -> Enciende LED de alarma.
 *   - Si el nivel supera  >  95% del volumen total -> Cierra la valvula (servo 0 grados).
 * ============================================================================
 */

#include <LiquidCrystal.h>   // Libreria estandar para LCD 16x2 paralelo (Tinkercad y Wokwi)
#include <Servo.h>           // Libreria estandar para controlar el servomotor (valvula)

// ==================== DEFINICION DE PINES ====================
// Pantalla LCD 16x2 en modo de 4 bits: LiquidCrystal(RS, E, D4, D5, D6, D7)
const int LCD_RS = 12;
const int LCD_E  = 11;
const int LCD_D4 = 5;
const int LCD_D5 = 4;
const int LCD_D6 = 3;
const int LCD_D7 = 2;

// Sensor Ultrasonico HC-SR04 - Tanque 1 (nivel h1)
const int TRIG_T1 = 6;
const int ECHO_T1 = 7;

// Sensor Ultrasonico HC-SR04 - Tanque 2 (nivel h2)
const int TRIG_T2 = 8;
const int ECHO_T2 = 9;

// Actuadores: Servomotor (Valvula de entrada qi) y LED de Alarma
const int PIN_SERVO_VALVULA = 10;
const int PIN_LED_ALARMA    = 13;

// ==================== PARAMETROS GEOMETRICOS DEL TANQUE ====================
const float ALTURA_TANQUE_CM   = 200.0;                 // 2.0 metros = 200 cm
const float RADIO_TANQUE_M     = 0.5;                   // 0.5 metros
const float AREA_BASE_M2       = PI * RADIO_TANQUE_M * RADIO_TANQUE_M; // ~0.785398 m^2
const float VOLUMEN_MAX_LITROS = AREA_BASE_M2 * (ALTURA_TANQUE_CM / 100.0) * 1000.0; // ~1570.80 L

// Umbrales de seguridad (%)
const float UMBRAL_ALARMA_PCT  = 90.0;                  // >= 90%: Enciende LED de alarma
const float UMBRAL_VALVULA_PCT = 95.0;                  // >  95%: Cierra valvula de entrada

// Angulos del servomotor que simula la valvula
const int VALVULA_ABIERTA = 90;                         // 90 grados = paso libre de liquido
const int VALVULA_CERRADA = 0;                          // 0 grados  = ingreso cerrado

// ==================== OBJETOS GLOBALES ====================
LiquidCrystal lcd(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7);
Servo valvula;

// ==================== FUNCION PARA MEDIR DISTANCIA CON HC-SR04 ====================
float medirDistanciaCm(int pinTrig, int pinEcho) {
  // Asegurar pulso limpio en TRIG
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);

  // Enviar pulso ultrasonico de 10 microsegundos
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  // Medir duracion del eco (timeout 25 ms -> cubre hasta ~425 cm)
  unsigned long duracionUs = pulseIn(pinEcho, HIGH, 25000UL);

  // Si no hubo eco (fuera de rango), asumir tanque vacio (>= 200 cm)
  if (duracionUs == 0) {
    return ALTURA_TANQUE_CM;
  }

  // Distancia (cm) = (duracion_us * 0.0343 cm/us) / 2
  float distanciaCm = (duracionUs * 0.0343) / 2.0;
  return distanciaCm;
}

// ==================== FUNCION DE CALCULO DE VOLUMEN ====================
void calcularTanque(float distanciaCm, float &alturaLiquidoCm, float &volumenLitros, float &porcentaje) {
  // El sensor esta en la tapa superior (200 cm sobre el fondo):
  // altura del liquido = Altura total - distancia medida al espejo de agua
  alturaLiquidoCm = ALTURA_TANQUE_CM - distanciaCm;

  // Limitar la altura al rango fisico valido [0, 200] cm
  if (alturaLiquidoCm < 0.0) {
    alturaLiquidoCm = 0.0;
  } else if (alturaLiquidoCm > ALTURA_TANQUE_CM) {
    alturaLiquidoCm = ALTURA_TANQUE_CM;
  }

  // Volumen en m^3 = Area_base(m^2) * altura(m); luego x 1000 para Litros
  volumenLitros = AREA_BASE_M2 * (alturaLiquidoCm / 100.0) * 1000.0;

  // Porcentaje de llenado respecto al volumen maximo del tanque
  porcentaje = (volumenLitros / VOLUMEN_MAX_LITROS) * 100.0;
}

// ==================== CONFIGURACION INICIAL ====================
void setup() {
  Serial.begin(9600);

  // Configurar pines de los sensores ultrasonicos
  pinMode(TRIG_T1, OUTPUT);
  pinMode(ECHO_T1, INPUT);
  pinMode(TRIG_T2, OUTPUT);
  pinMode(ECHO_T2, INPUT);

  // Configurar LED de alarma
  pinMode(PIN_LED_ALARMA, OUTPUT);
  digitalWrite(PIN_LED_ALARMA, LOW);

  // Inicializar servomotor en posicion de valvula abierta
  valvula.attach(PIN_SERVO_VALVULA);
  valvula.write(VALVULA_ABIERTA);

  // Inicializar pantalla LCD 16x2 con mensaje de bienvenida
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("SISTEMA TANQUES");
  lcd.setCursor(0, 1);
  lcd.print("UPT IoT - U2");
  delay(1500);
  lcd.clear();

  Serial.println("=== MONITOR DE NIVEL DE DOS TANQUES (H=2m, R=0.5m) ===");
  Serial.print("Volumen maximo por tanque: ");
  Serial.print(VOLUMEN_MAX_LITROS, 1);
  Serial.println(" L");
}

// ==================== BUCLE PRINCIPAL ====================
void loop() {
  // 1. Medir distancia en el Tanque 1 (espera breve entre sensores para evitar eco cruzado)
  float dist1 = medirDistanciaCm(TRIG_T1, ECHO_T1);
  delay(35);

  // 2. Medir distancia en el Tanque 2
  float dist2 = medirDistanciaCm(TRIG_T2, ECHO_T2);

  // 3. Calcular altura de liquido, volumen (L) y porcentaje (%) para cada tanque
  float h1, vol1, pct1;
  float h2, vol2, pct2;
  calcularTanque(dist1, h1, vol1, pct1);
  calcularTanque(dist2, h2, vol2, pct2);

  // Volumen total combinado de ambos tanques
  float volTotalSistema = vol1 + vol2;
  float pctTotalSistema = (volTotalSistema / (2.0 * VOLUMEN_MAX_LITROS)) * 100.0;

  // 4. Logica de Alarma (>= 90% en cualquiera de los tanques)
  bool alarmaActiva = (pct1 >= UMBRAL_ALARMA_PCT) || (pct2 >= UMBRAL_ALARMA_PCT);
  digitalWrite(PIN_LED_ALARMA, alarmaActiva ? HIGH : LOW);

  // 5. Logica de Valvula de Entrada (> 95% en cualquiera de los tanques cierra la valvula)
  bool cerrarValvula = (pct1 > UMBRAL_VALVULA_PCT) || (pct2 > UMBRAL_VALVULA_PCT);
  valvula.write(cerrarValvula ? VALVULA_CERRADA : VALVULA_ABIERTA);

  // 6. Mostrar resultados en el Display LCD 16x2 (formato fijo de 16 caracteres por fila)
  //    Fila 0: T1:1414L  90% AB   (AB = Valvula Abierta, CE = Valvula Cerrada)
  //    Fila 1: T2:1257L  80% AL   (OK = Normal, AL = Alarma >= 90%)
  char linea0[17];
  char linea1[17];
  int vol1Int = (int)(vol1 + 0.5);
  int pct1Int = (int)(pct1 + 0.5);
  int vol2Int = (int)(vol2 + 0.5);
  int pct2Int = (int)(pct2 + 0.5);

  snprintf(linea0, sizeof(linea0), "T1:%4dL %3d%% %s", vol1Int, pct1Int, cerrarValvula ? "CE" : "AB");
  snprintf(linea1, sizeof(linea1), "T2:%4dL %3d%% %s", vol2Int, pct2Int, alarmaActiva ? "AL" : "OK");

  lcd.setCursor(0, 0);
  lcd.print(linea0);
  lcd.setCursor(0, 1);
  lcd.print(linea1);

  // 7. Reporte detallado por Monitor Serie
  Serial.print("T1: h="); Serial.print(h1, 1); Serial.print("cm | V=");
  Serial.print(vol1, 1); Serial.print("L ("); Serial.print(pct1, 1); Serial.print("%)  ||  ");
  Serial.print("T2: h="); Serial.print(h2, 1); Serial.print("cm | V=");
  Serial.print(vol2, 1); Serial.print("L ("); Serial.print(pct2, 1); Serial.print("%)  ||  ");
  Serial.print("Total="); Serial.print(volTotalSistema, 1); Serial.print("L (");
  Serial.print(pctTotalSistema, 1); Serial.print("%) | LED=");
  Serial.print(alarmaActiva ? "ON" : "OFF");
  Serial.print(" | Valvula=");
  Serial.println(cerrarValvula ? "CERRADA (0 deg)" : "ABIERTA (90 deg)");

  delay(300);
}
