/*
 * Guía de Laboratorio Nº10 / Lab 2.5: "PLACA ESP32 CON THINGSPEAK"
 * Medición de Nivel de Agua en Tanque Cilíndrico y Telemetría IoT
 * Universidad Privada de Tacna - Escuela de Ingeniería de Sistemas
 * Docente: Mgr. Alex Juan Yanqui Constancio
 * Autores: Perez Fabrizio - Arocutipa Gian Franco
 */

#include <Wire.h> 
#include <LiquidCrystal_I2C.h> 
#include <WiFi.h> 
#include <ThingSpeak.h> 
 
// ==================== CONFIGURACIÓN WIFI ====================
const char* WIFI_SSID = "Wokwi-GUEST";   
const char* WIFI_PASS = "";    
 
// ================= CONFIGURACIÓN THINGSPEAK =================
// Credenciales oficiales de la guía de laboratorio
unsigned long CHANNEL_ID = 3440423;              
const char* WRITE_API_KEY = "D67PP21TA1CXR5XI"; 
 
// ================== CONFIGURACIÓN DE PINES ==================
const int PIN_TRIG = 5;       // Trigger HC-SR04
const int PIN_ECHO = 18;      // Echo HC-SR04
const int PIN_LED  = 2;       // LED indicador de alarma (> 90%)
 
// ============== CONFIGURACIÓN TANQUE CILÍNDRICO ==============
// Tanque: 1 metro de alto (100 cm), 0.5 metros de radio (50 cm)
const float ALTURA_TANQUE = 100.0;  // cm
const float RADIO_TANQUE  = 50.0;   // cm
const float PI_CONST      = 3.14159265; 
 
// ================= INICIALIZACIÓN DE OBJETOS =================
// Pantalla LCD 16x2 vía I2C (Dirección estándar 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2);  
WiFiClient client; 
 
// Temporizador de envío a ThingSpeak (Mínimo 15s para plan gratuito)
unsigned long ultimoEnvio = 0; 
const unsigned long INTERVALO_ENVIO = 15000; // 15 segundos 
 
void setup() { 
  Serial.begin(115200); 
  Serial.println("\n--- INICIANDO SISTEMA DE MEDICION DE NIVEL ---"); 
 
  pinMode(PIN_TRIG, OUTPUT); 
  pinMode(PIN_ECHO, INPUT); 
  pinMode(PIN_LED, OUTPUT); 
 
  // Inicialización de la pantalla LCD
  lcd.init(); 
  lcd.backlight(); 
   
  // Conexión WiFi en Wokwi
  lcd.setCursor(0, 0); 
  lcd.print("Conectando WiFi"); 
  WiFi.begin(WIFI_SSID, WIFI_PASS); 
   
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500); 
    Serial.print("."); 
  } 
   
  Serial.println("\nWiFi Conectado!"); 
  lcd.clear(); 
  lcd.print("WiFi Conectado"); 
  delay(1500); 
  lcd.clear(); 
 
  // Inicialización del cliente ThingSpeak
  ThingSpeak.begin(client); 
} 
 
void loop() { 
  // --- 1. MEDICIÓN DE DISTANCIA CON HC-SR04 --- 
  digitalWrite(PIN_TRIG, LOW); 
  delayMicroseconds(2); 
  digitalWrite(PIN_TRIG, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(PIN_TRIG, LOW); 
 
  long duracion = pulseIn(PIN_ECHO, HIGH); 
  // Velocidad del sonido = 0.0343 cm/us (ida y vuelta / 2)
  float distancia_vacio = duracion * 0.0343 / 2.0; 
 
  // --- 2. CÁLCULO DE NIVEL Y VOLUMEN --- 
  float nivel_agua = ALTURA_TANQUE - distancia_vacio;  
   
  // Limitación para evitar lecturas falsas por rebotes acústicos
  if (nivel_agua < 0) nivel_agua = 0; 
  if (nivel_agua > ALTURA_TANQUE) nivel_agua = ALTURA_TANQUE; 
 
  // Volumen Cilindro: V = pi * r^2 * h (en cm3). 1 L = 1000 cm3
  float volumen_cm3 = PI_CONST * (RADIO_TANQUE * RADIO_TANQUE) * nivel_agua; 
  float volumen_litros = volumen_cm3 / 1000.0; 
  float porcentaje = (nivel_agua / ALTURA_TANQUE) * 100.0; 
 
  // --- 3. CONTROL DE ALARMA (> 90%) --- 
  if (porcentaje > 90.0) { 
    digitalWrite(PIN_LED, HIGH); 
  } else { 
    digitalWrite(PIN_LED, LOW); 
  } 
 
  // --- 4. VISUALIZACIÓN EN LCD 16X2 --- 
  lcd.setCursor(0, 0); 
  lcd.print("Vol: "); 
  lcd.print(volumen_litros, 1); 
  lcd.print(" L       "); // Espacios para limpiar dígitos sobrantes
 
  lcd.setCursor(0, 1); 
  lcd.print("Nivel: "); 
  lcd.print(porcentaje, 1); 
  lcd.print("% "); 
  if (porcentaje > 90.0) { 
    lcd.print("!ALTA!"); 
  } else { 
    lcd.print("      "); 
  } 
 
  // --- 5. MONITOREO SERIAL LOCAL ---
  Serial.print("Dist. Vacio: "); Serial.print(distancia_vacio, 1);
  Serial.print(" cm | Nivel: "); Serial.print(nivel_agua, 1);
  Serial.print(" cm | Vol: "); Serial.print(volumen_litros, 1);
  Serial.print(" L | Porc: "); Serial.print(porcentaje, 1);
  Serial.println("%");
 
  // --- 6. ENVÍO DE TELEMETRÍA A THINGSPEAK (CADA 15s) --- 
  if (millis() - ultimoEnvio >= INTERVALO_ENVIO) { 
    if (WiFi.status() != WL_CONNECTED) { 
      Serial.println("Reconectando a WiFi..."); 
      WiFi.disconnect(); 
      WiFi.reconnect(); 
    } else { 
      // Configuración de los canales de ThingSpeak
      ThingSpeak.setField(1, volumen_litros); // Campo 1: Volumen en Litros 
      ThingSpeak.setField(2, porcentaje);     // Campo 2: Porcentaje de llenado 
 
      // Transmisión HTTP a los servidores de ThingSpeak
      int respuesta = ThingSpeak.writeFields(CHANNEL_ID, WRITE_API_KEY); 
 
      if (respuesta == 200) { 
        Serial.println(">> [ThingSpeak] ¡Datos enviados correctamente! (HTTP 200)"); 
      } else { 
        Serial.print(">> [ThingSpeak] Error en envío. Código HTTP: "); 
        Serial.println(respuesta); 
      } 
    } 
    ultimoEnvio = millis(); 
  } 
 
  delay(200); // Frecuencia de actualización en pantalla local
}
