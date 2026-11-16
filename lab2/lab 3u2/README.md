# Laboratorio 2.3 (Lab 3U2): Placa ESP32, Sensores y Cloud IoT Adafruit

**Universidad Privada de Tacna**  
**Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas  
**Docente:** Mgr. Alex Juan Yanqui Constancio  

**Integrantes:**
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790

---

## Contenido del Laboratorio

Esta carpeta contiene todos los informes académicos formales, los esquemas y códigos funcionales listos para simular en Wokwi y conectar a Adafruit IO:

```
lab 3u2/
│
├── lab 3u2.docx                                                   # Informe final en formato Word
├── lab 3.docx                                                     # Copia directa
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx
├── Lab 2.3 - Esp32 Wokwi - Adafruit.pdf                           # Guía oficial del docente
├── TODOS_LOS_EJERCICIOS_WOKWI_LAB3.txt                            # Códigos unificados para Wokwi
│
├── 01_Circuito1_HolaMundo_ESP32/                                  # Circuito 1: UART0 y Setup/Loop
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 02_Circuito2_Semaforo_Leds_ESP32/                              # Circuito 2: Semáforo de 3 LEDs
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 03_Circuito3_Sensor_DHT22_Potenciometro/                       # Circuito 3: DHT22 + ADC 12 bits
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   └── README.md
│
├── 04_Circuito4_ESP32_WiFi_Adafruit_IO_MQTT/                      # Circuito 4: Conexión WiFi + MQTT
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   └── README.md
│
└── 05_Circuito5_Cuestionario_Integrador_Adafruit_5Feeds/          # Circuito 5: Cuestionario Resuelto
    ├── sketch.ino                                                 # 5 Feeds simultáneos en Adafruit IO
    ├── diagram.json                                               # ESP32 + DHT22 + 2 Potenciómetros
    ├── libraries.txt
    └── README.md
```

---

## Guía Rápida para Simular en Wokwi (https://wokwi.com)
1. Para cualquiera de los circuitos, abre Wokwi y crea un nuevo proyecto con **ESP32**.
2. Copia y pega el contenido de `sketch.ino` en la pestaña de código.
3. Copia y pega `diagram.json` en la pestaña del diagrama.
4. Si el circuito requiere librerías (Circuitos 3, 4 y 5), agrega el contenido de `libraries.txt` en el administrador de librerías.
5. Presiona **Play**:
   - En el Circuito 4 y 5, el ESP32 se conectará a la red Wi-Fi simulada `Wokwi-GUEST` y comenzará a enviar los datos vía MQTT al servidor `io.adafruit.com`.
