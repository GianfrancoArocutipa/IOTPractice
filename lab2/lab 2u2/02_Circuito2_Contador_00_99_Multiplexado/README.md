# Circuito 2: Contador 00 a 99 Multiplexado con Transistores 2N2222 (Arduino Nano)

## Descripción
Contador de dos dígitos de 00 a 99 con refresco por multiplexación temporal (~125 Hz).
- Pin D9: Base del Transistor 1 (control del display izquierdo de Decenas).
- Pin D10: Base del Transistor 2 (control del display derecho de Unidades).
- Pines D2 a D8: Bus compartido de segmentos a..g con resistencias de 220 Ω.

## Corrección clave
Se eliminaron los puentes directos a GND que cortocircuitaban los cátodos comunes en el diseño original, permitiendo la conmutación independiente de cada transistor.

## Instrucciones en Wokwi
1. Pega `sketch.ino` y `diagram.json`.
2. Crea los archivos del chip con el botón '+' en Wokwi:
   - `2n2222.chip.json`
   - `2n2222.chip.c`
3. Presiona Play y observa el conteo nítido de 00 a 99 sin superposiciones ni parpadeo.
