const byte num[10][7] = {
  {1,1,1,1,1,1,0}, {0,1,1,0,0,0,0}, {1,1,0,1,1,0,1}, {1,1,1,1,0,0,1}, {0,1,1,0,0,1,1},
  {1,0,1,1,0,1,1}, {1,0,1,1,1,1,1}, {1,1,1,0,0,0,0}, {1,1,1,1,1,1,1}, {1,1,1,1,0,1,1}
};

int dist = 0, dig[3] = {0, 0, 0}, d = 0;
unsigned long tSens = 0, tMux = 0, tLed = 0;
bool vEst = false;

void setup() {
  for (int p = 2; p <= 12; p++) pinMode(p, OUTPUT);
  for (int p = 9; p <= 11; p++) digitalWrite(p, HIGH);
  pinMode(13, INPUT);
  pinMode(A0, OUTPUT); pinMode(A1, OUTPUT); pinMode(A2, OUTPUT); pinMode(A3, OUTPUT);
}

void loop() {
  unsigned long ms = millis();

  if (ms - tSens >= 150) {
    tSens = ms;
    for (int p = 9; p <= 11; p++) digitalWrite(p, HIGH);
    digitalWrite(12, LOW);  delayMicroseconds(2);
    digitalWrite(12, HIGH); delayMicroseconds(10);
    digitalWrite(12, LOW);
    long t = pulseIn(13, HIGH, 23000);
    dist = (t == 0) ? 330 : constrain((int)((t * 0.0343) / 2.0 + 0.5), 0, 330);
    dig[0] = (dist / 100) % 10;
    dig[1] = (dist / 10) % 10;
    dig[2] = dist % 10;
  }

  if (dist > 300) {
    if (ms - tLed >= 300) { tLed = ms; vEst = !vEst; }
    digitalWrite(A0, vEst); digitalWrite(A1, LOW); digitalWrite(A2, LOW);
    noTone(A3);
  } else if (dist >= 100) {
    digitalWrite(A0, LOW); digitalWrite(A1, HIGH); digitalWrite(A2, LOW);
    noTone(A3);
  } else {
    digitalWrite(A0, LOW); digitalWrite(A1, LOW); digitalWrite(A2, HIGH);
    tone(A3, 1200);
  }

  if (ms - tMux >= 4) {
    tMux = ms;
    for (int p = 9; p <= 11; p++) digitalWrite(p, HIGH);
    for (int s = 0; s < 7; s++) digitalWrite(2 + s, num[dig[d]][s]);
    digitalWrite(9 + d, LOW);
    d = (d + 1) % 3;
  }
}
