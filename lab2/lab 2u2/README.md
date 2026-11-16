# Laboratorio 2 - Unidad 2 (Lab 2U2): Arduino Nano, Displays 7 Segmentos, Multiplexación y DHT22

**Universidad Privada de Tacna**  
**Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas  
**Docente:** Mgr. Alex Juan Yanqui Constancio  

**Integrantes:**
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790

---

## Estructura de la Carpeta `lab 2u2`

Esta carpeta contiene la totalidad de los entregables, códigos funcionales de simulación en Wokwi, guías y el informe académico formal:

```
lab 2u2/
│
├── lab 2u2.docx                                                   # Informe final completo en formato Word
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2u2 Arduino Nano Wokwi.docx
├── Lab 2.2 Arduino Nano Wokwi.pdf                                 # Guía oficial del docente
├── TODOS_LOS_EJERCICIOS_WOKWI.txt                                 # Archivo unificado de códigos y esquemas Wokwi
│
├── 01_Circuito1_Contador_0_9/                                     # Circuito 1: Contador 0 a 9 en 1 Display
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 02_Circuito2_Contador_00_99_Multiplexado/                      # Circuito 2: Contador 00 a 99 multiplexado
│   ├── sketch.ino
│   ├── diagram.json
│   ├── 2n2222.chip.json                                           # Definición del Custom Chip 2N2222
│   ├── 2n2222.chip.c                                              # Lógica de conmutación en lenguaje C
│   └── README.md
│
├── 03_Circuito3_Sensor_DHT22_Multiplexado/                        # Circuito 3: Sensor DHT22 + Multiplexación
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   ├── 2n2222.chip.json
│   ├── 2n2222.chip.c
│   └── README.md
│
├── scripts_informe/                                               # Script generador en Python y plantillas
│   ├── generate_final_report.py
│   └── extracted_assets/
│
└── archivos_texto_originales/                                     # Registros y anotaciones de depuración
    ├── 02_Circuito1_Contador_0_9_Nano.txt
    ├── 03_Circuito2_Contador_00_99_Multiplexado_Nano.txt
    └── 04_Circuito3_Sensor_DHT22_Nano.txt
```

---

## Resumen Técnico de los Circuitos

1. **Circuito 1: Contador de 0 a 9**
   - Manejo del display de 7 segmentos de cátodo común mediante los pines D2 a D8.
   - Activación controlada del transistor derecho (Pin D10 = HIGH) para permitir conteo limpio en una sola pantalla.

2. **Circuito 2: Contador 00 a 99 Multiplexado**
   - Conmutación rápida (~125 Hz) de dos displays mediante transistores NPN 2N2222 gobernados por los pines D9 (decenas) y D10 (unidades).
   - Aprovechamiento del fenómeno POV (Persistencia de la Visión) para lograr visión simultánea libre de parpadeo.
   - Solución del error de cortocircuito a GND retirando los puentes redundantes.

3. **Circuito 3: Sensor Digital DHT22 con Visualización en Displays**
   - Lectura digital unifilar de temperatura y humedad ambiental (Pin D11).
   - Conversión de grados Celsius a dígitos individuales (decenas y unidades).
   - Despliegue en tiempo real en los displays de 7 segmentos y monitoreo continuo por puerto serial a 9600 baudios.
