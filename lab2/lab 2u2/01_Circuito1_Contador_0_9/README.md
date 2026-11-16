# Circuito 1: Contador de 0 a 9 con Display de 7 Segmentos (Arduino Nano)

## Descripción
Control de un display de 7 segmentos de cátodo común mostrando el conteo cíclico de 0 a 9.
Adaptado para la configuración con transistores NPN 2N2222:
- Pin D10 en HIGH: Habilita el transistor del display derecho (unidades).
- Pin D9 en LOW: Mantiene apagado el display izquierdo.

## Instrucciones en Wokwi (https://wokwi.com)
1. Pega `sketch.ino` en la pestaña de código.
2. Pega `diagram.json` en la pestaña del diagrama.
3. Presiona Play para ver el conteo de 0 a 9 cada 600 ms.
