#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo valvula;

float medirCm(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long t = pulseIn(echo, HIGH, 25000);
  return t == 0 ? 200.0 : (t * 0.0343) / 2.0;
}

void setup() {
  pinMode(6, OUTPUT); pinMode(7, INPUT);
  pinMode(8, OUTPUT); pinMode(9, INPUT);
  pinMode(13, OUTPUT);
  valvula.attach(10);
  valvula.write(90);
  lcd.begin(16, 2);
}

void loop() {
  float h1 = constrain(200.0 - medirCm(6, 7), 0.0, 200.0);
  delay(35);
  float h2 = constrain(200.0 - medirCm(8, 9), 0.0, 200.0);

  float v1 = PI * 0.25 * (h1 / 100.0) * 1000.0;
  float v2 = PI * 0.25 * (h2 / 100.0) * 1000.0;
  float p1 = (h1 / 200.0) * 100.0;
  float p2 = (h2 / 200.0) * 100.0;

  digitalWrite(13, (p1 >= 90.0 || p2 >= 90.0) ? HIGH : LOW);
  valvula.write((p1 > 95.0 || p2 > 95.0) ? 0 : 90);

  lcd.setCursor(0, 0);
  lcd.print("T1: "); lcd.print((int)v1); lcd.print(" L     ");
  lcd.setCursor(0, 1);
  lcd.print("T2: "); lcd.print((int)v2); lcd.print(" L     ");
  delay(300);
}
