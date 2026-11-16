# Circuito 5: Cuestionario Integrador - 5 Feeds en Adafruit IO (ESP32)

## Descripción
Resolución completa del ejercicio integrador de la guía: publicación simultánea de Temperatura, Humedad, Sensación Térmica, Potenciómetro 1 (GPIO 34) y Potenciómetro 2 (GPIO 35).

## Aspecto Clave de Hardware
Ambos potenciómetros se conectan al ADC1 (GPIO 34 y 35) para evitar el conflicto de hardware del ADC2 con el módem Wi-Fi activo.

## Instrucciones en Wokwi
1. Pega `sketch.ino` y `diagram.json`.
2. En `libraries.txt`, incluye las librerías requeridas.
3. Inicia la simulación para alimentar los 5 feeds en tu Dashboard.
