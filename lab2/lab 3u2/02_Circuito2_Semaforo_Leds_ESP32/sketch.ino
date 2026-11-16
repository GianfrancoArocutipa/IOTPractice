// CIRCUITO 2: CONTROL DE SEMÁFORO DE 3 LEDS - ESP32
#define verde 18       // GPIO 18 -> LED Verde
#define rojo 21        // GPIO 21 -> LED Rojo
#define amarillo 22    // GPIO 22 -> LED Amarillo

void setup() {
  Serial.begin(115200);
  pinMode(verde, OUTPUT);
  pinMode(rojo, OUTPUT);
  pinMode(amarillo, OUTPUT);
}

void loop() {
  digitalWrite(verde, HIGH);
  Serial.println("Led Verde ON ");
  delay(1000);

  digitalWrite(rojo, HIGH);
  Serial.println("Led rojo ON ");
  delay(1000);

  digitalWrite(amarillo, HIGH);
  Serial.println("Led amarillo ON ");
  delay(1000);

  digitalWrite(verde, LOW);
  Serial.println("Led VERDE OFF ");
  delay(1000);

  digitalWrite(rojo, LOW);
  Serial.println("Led ROJO OFF ");
  delay(1000);

  digitalWrite(amarillo, LOW);
  Serial.println("Led AMARILLO OFF ");
  delay(1000);
}
