// CIRCUITO 1: HOLA MUNDO - ESP32
void setup() {
  Serial.begin(115200);  // Inicialización serial estándar ESP32
  Serial.println("Esta linea se ejecuta en el void setup.");
  Serial.println("esta es una segunda linea del void setup.");
}

void loop() {
  Serial.println(" Esta linea pertenece al void loop  ");
  Serial.println(" En otra linea --- Hola Mundo ---");
  delay(2000);
}
