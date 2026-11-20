#include <LiquidCrystal.h>
#include <Servo.h>

// Pines del LCD 16x2 (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Pines de los sensores HC-SR04 (Tanque 1 y Tanque 2)
const int trigTanque1 = 6;
const int echoTanque1 = 7;
const int trigTanque2 = 8;
const int echoTanque2 = 9;

// Pines de la valvula (servo) y LED de alarma
const int pinServo  = 10;
const int ledAlarma = 13;

// Dimensiones de cada tanque (2 m de alto y 0.5 m de radio)
const float alturaTanqueCm = 200.0;
const float radioTanqueM   = 0.5;
const float areaBaseM2     = PI * radioTanqueM * radioTanqueM;
const float volumenTotalL  = areaBaseM2 * 2.0 * 1000.0; // ~1570.8 litros

Servo valvula;

float medirDistanciaCm(int pinTrig, int pinEcho) {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  unsigned long duracion = pulseIn(pinEcho, HIGH, 25000);
  if (duracion == 0) {
    return alturaTanqueCm;
  }
  return (duracion * 0.0343) / 2.0;
}

void setup() {
  pinMode(trigTanque1, OUTPUT);
  pinMode(echoTanque1, INPUT);
  pinMode(trigTanque2, OUTPUT);
  pinMode(echoTanque2, INPUT);
  pinMode(ledAlarma, OUTPUT);

  valvula.attach(pinServo);
  valvula.write(90); // Valvula abierta

  lcd.begin(16, 2);
}

void loop() {
  // Medir distancia en ambos tanques
  float distancia1 = medirDistanciaCm(trigTanque1, echoTanque1);
  delay(35);
  float distancia2 = medirDistanciaCm(trigTanque2, echoTanque2);

  // Calcular altura del liquido (cm)
  float altura1 = constrain(alturaTanqueCm - distancia1, 0.0, alturaTanqueCm);
  float altura2 = constrain(alturaTanqueCm - distancia2, 0.0, alturaTanqueCm);

  // Calcular volumen en litros y porcentaje de cada tanque
  float volumen1    = areaBaseM2 * (altura1 / 100.0) * 1000.0;
  float volumen2    = areaBaseM2 * (altura2 / 100.0) * 1000.0;
  float porcentaje1 = (volumen1 / volumenTotalL) * 100.0;
  float porcentaje2 = (volumen2 / volumenTotalL) * 100.0;

  // Encender LED de alarma al llegar al 90%
  if (porcentaje1 >= 90.0 || porcentaje2 >= 90.0) {
    digitalWrite(ledAlarma, HIGH);
  } else {
    digitalWrite(ledAlarma, LOW);
  }

  // Cerrar valvula de entrada al pasar el 95%
  if (porcentaje1 > 95.0 || porcentaje2 > 95.0) {
    valvula.write(0);  // Cerrada
  } else {
    valvula.write(90); // Abierta
  }

  // Mostrar volumen de ambos tanques en el LCD
  lcd.setCursor(0, 0);
  lcd.print("Tanque 1:");
  lcd.print((int)volumen1);
  lcd.print("L   ");

  lcd.setCursor(0, 1);
  lcd.print("Tanque 2:");
  lcd.print((int)volumen2);
  lcd.print("L   ");

  delay(300);
}
