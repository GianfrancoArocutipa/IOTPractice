const int segE[5] = {A1, A2, A3, A4, A5};
bool alarma = false;

void setup() {
  for (int p = 2; p <= 11; p++) pinMode(p, OUTPUT);
  for (int i = 0; i < 5; i++) pinMode(segE[i], OUTPUT);
  pinMode(12, INPUT_PULLUP);
  pinMode(13, OUTPUT);
}

void loop() {
  float v = analogRead(A0) * (5.0 / 1024.0);
  float temp = (v - 0.5) * 100.0;

  int led = -1;
  if (temp >= 9.5) {
    led = constrain((int)round((temp - 10.0) * 9.0 / 30.0), 0, 9);
  }

  for (int i = 0; i < 10; i++) {
    digitalWrite(2 + i, (i == led) ? HIGH : LOW);
  }

  if (led == 9) alarma = true;
  if (digitalRead(12) == LOW && led < 9) alarma = false;

  for (int i = 0; i < 5; i++) {
    digitalWrite(segE[i], alarma ? HIGH : LOW);
  }
  if (alarma) tone(13, 1000);
  else noTone(13);

  delay(50);
}
