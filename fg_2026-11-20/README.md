# Examen de Unidad 2 — Internet de las Cosas (IoT)

- **Universidad:** Universidad Privada de Tacna (UPT) — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
- **Curso:** Internet de las Cosas (Ciclo 2026 - II)
- **Docente:** Ing. Alex Yanqui Constancio
- **Autores:** Fabrizio Salvador Elias Perez Peralta y Gian Franco Arocutipa Arocutipa
- **Fecha:** 2026-11-20

---

## Contenido de la Carpeta (`fg_2026-11-20`)

| N° | Carpeta / Archivo | Descripción del Proyecto | Microcontrolador |
| :---: | :--- | :--- | :---: |
| **1** | [`ejercicio1_nivel_tanques/`](./ejercicio1_nivel_tanques/README.md) | Medición de nivel y volumen en dos tanques cilíndricos ($H = 2\text{ m}$, $R = 0.5\text{ m}$) con 2 sensores HC-SR04, pantalla LCD 16×2, LED de alarma ($\ge 90\%$) y servomotor como válvula de entrada ($> 95\%$ cierra). | Arduino Uno R3 |
| **2** | [`ejercicio2_monitor_temperatura/`](./ejercicio2_monitor_temperatura/README.md) | Monitor de temperatura de precisión ($10\,^\circ\text{C}$ a $40\,^\circ\text{C}$) con sensor TMP36, 10 LEDs en **modo punto**, alarma sonora enclavada al llegar al LED 10, pulsador de reinicio (`reset`) y display de 7 segmentos mostrando **`E`**. | Arduino Uno R3 |
| **3** | [`ejercicio3_estacionamiento_hcsr04/`](./ejercicio3_estacionamiento_hcsr04/README.md) | Asistente de estacionamiento con HC-SR04 ($0$–$330\text{ cm}$), 3 displays de 7 segmentos multiplexados, LED verde parpadeando ($> 3.0\text{ m}$), LED naranja ($1.0\text{ m}$–$3.0\text{ m}$), LED rojo + alarma sonora ($< 1.0\text{ m}$). | Arduino Uno R3 |
| **Word** | [`Examen_Unidad2_IoT_Resuelto.docx`](./Examen_Unidad2_IoT_Resuelto.docx) | Documento formal en Microsoft Word con los 3 ejercicios desarrollados: análisis técnico, materiales, tablas pin a pin, guía paso a paso para Tinkercad, código detallado línea por línea y espacios reservados para capturas y enlaces de Tinkercad. | — |

---

## Compatibilidad de Simulación

Todos los códigos (`sketch.ino`) fueron diseñados y verificados para funcionar **sin modificaciones** en:
1. **Autodesk Tinkercad Circuits** (editor de **Código → Texto**).
2. **Wokwi Simulator** (importando `sketch.ino` + `diagram.json` de cada ejercicio).

> **Nota sobre Ejercicio 2 en Wokwi:** Tinkercad cuenta con el sensor nativo **TMP36** (usado directamente en el código y en la guía de Tinkercad). Dado que Wokwi no dispone de un componente TMP36 nativo, el archivo `diagram.json` de Wokwi incluye un potenciómetro con divisor resistivo calibrado ($0.53\text{ V}$ a $1.02\text{ V}$) que emula el voltaje analógico exacto del TMP36 para probar el mismo `sketch.ino`.
