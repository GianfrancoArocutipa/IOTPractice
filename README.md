# IOTPractice - Prácticas de Internet de las Cosas (IoT)

**Universidad Privada de Tacna**  
**Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas (IoT)  
**Docente:** Mgr. Alex Juan Yanqui Constancio  
**Estudiante:** Gian Franco Arocutipa Arocutipa / Fabrizio Perez Peralta  

---

## 📂 Contenido del Repositorio

Este repositorio reúne las prácticas de laboratorio, simulaciones interactivas en Wokwi, telemetría IoT en la nube y trabajos de investigación del curso:

### 1. [Lab2.5_ESP32_ThingSpeak](./Lab2.5_ESP32_ThingSpeak)
- **Tema:** Medición de nivel y volumen en un tanque de agua cilíndrico ($H = 100\text{ cm}, R = 50\text{ cm}$, $\approx 785.4\text{ L}$).
- **Hardware en Wokwi:** ESP32 DevKit V1, Sensor Ultrasónico HC-SR04, Pantalla LCD 16x2 (I2C), LED de alarma ($> 90\%$).
- **Cloud IoT:** MathWorks ThingSpeak (Canal 3440423, envío de volumen y porcentaje cada 15 segundos).

### 2. [lab2](./lab2) — Arduino Nano y Multiplexación
- **Circuito 1:** Contador de 0 a 9 en display de 7 segmentos de cátodo común.
- **Circuito 2:** Contador 00 a 99 multiplexado mediante transistores 2N2222 (Persistencia de la Visión - POV).
- **Circuito 3:** Sensor digital DHT22 con despliegue de temperatura en displays multiplexados.
- **Custom Chip:** Simulación de transistores 2N2222 en Wokwi (`2n2222.chip.json` y `2n2222.chip.c`).

### 3. [lab3](./lab3) — ESP32 y Adafruit IO MQTT
- Hola Mundo ESP32, Semáforo LED.
- Sensor DHT22 + Potenciómetro.
- Conectividad WiFi y protocolo MQTT con Adafruit IO (5 feeds de telemetría y control remoto).

### 4. [Grupal](./Grupal) — Investigación de Brokers MQTT en la Nube
- Monografía formal sobre el protocolo MQTT y brokers en la nube.
- Presentación ejecutiva PPTX.
- Guía de exposición de las diapositivas 5 a la 8 con guion detallado y audios de práctica.

### 5. [Lab01](./Lab01) y [lab4](./lab4)
- Guías de laboratorio, scripts de extracción y reportes complementarios.
