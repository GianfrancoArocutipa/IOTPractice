# Circuito 3: Sensor DHT22 con Visualización Multiplexada en Displays de 7 Segmentos

## Descripción
Medición de temperatura ambiental con sensor digital DHT22 (Pin D11) y visualización en tiempo real en 2 displays de 7 segmentos multiplexados mediante transistores 2N2222.
- Reporte periódico por Monitor Serial (9600 baudios).
- Visualización instantánea del valor en grados Celsius (°C).

## Instrucciones en Wokwi
1. Pega `sketch.ino` y `diagram.json`.
2. En `libraries.txt`, añade:
   ```
   DHT sensor library
   ```
3. Crea los dos archivos del Custom Chip 2N2222:
   - `2n2222.chip.json`
   - `2n2222.chip.c`
4. Presiona Play:
   - Los displays mostrarán la temperatura inicial (24°C).
   - Haz clic en el sensor DHT22 durante la simulación y desliza el control de temperatura para verificar la actualización dinámica.
