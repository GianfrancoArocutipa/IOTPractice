# Ejercicio 2 — Monitor de Temperatura de Precisión (10 °C a 40 °C) en Modo Punto con Alarma Enclavada y Display "E"

## 1. Carátula del Laboratorio
- **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
- **Curso:** Internet de las Cosas (IoT) — Examen de Unidad 2 (Ciclo 2026 - II)
- **Docente:** Ing. Alex Yanqui Constancio
- **Autores:** Fabrizio Salvador Elias Perez Peralta y Gian Franco Arocutipa Arocutipa
- **Fecha:** 2026-11-20
- **Resumen del funcionamiento:** Monitor térmico de precisión en Arduino Uno que lee el sensor analógico **TMP36** en el rango de **$10\,^\circ\text{C}$ a $40\,^\circ\text{C}$** y enciende únicamente el LED correspondiente al intervalo actual (**modo punto**) entre 10 LEDs. Cuando la temperatura alcanza el **LED 10 ($40\,^\circ\text{C}$)**, se activa y **enclava** una alarma sonora en el buzzer y se enciende un **display de 7 segmentos mostrando la letra `E` (Error)**; ambos permanecen activos aunque la temperatura descienda, hasta que el usuario presione el **pulsador de reinicio (`RESET`)**.

---

## 2. Conversión del Sensor TMP36 e Intervalos de los 10 LEDs
El sensor **TMP36** entrega un voltaje lineal con un offset de $500\text{ mV}$ a $0\,^\circ\text{C}$ y una pendiente de $10\text{ mV}/^\circ\text{C}$:
$$V = \text{ADC} \times \frac{5.0}{1024.0} \qquad \Longrightarrow \qquad T(^\circ\text{C}) = (V - 0.5) \times 100$$

| LED | Pin Arduino | Color Sugerido | Temperatura Central | Rango de Activación | Acción Especial |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **LED 1** | `D2` | Verde | $10.0\,^\circ\text{C}$ | $9.5\,^\circ\text{C}$ a $11.6\,^\circ\text{C}$ | Indicador mínimo ($10\,^\circ\text{C}$) |
| **LED 2** | `D3` | Verde | $13.3\,^\circ\text{C}$ | $11.7\,^\circ\text{C}$ a $14.9\,^\circ\text{C}$ | Modo punto |
| **LED 3** | `D4` | Verde | $16.7\,^\circ\text{C}$ | $15.0\,^\circ\text{C}$ a $18.3\,^\circ\text{C}$ | Modo punto |
| **LED 4** | `D5` | Verde | $20.0\,^\circ\text{C}$ | $18.4\,^\circ\text{C}$ a $21.6\,^\circ\text{C}$ | Modo punto |
| **LED 5** | `D6` | Amarillo | $23.3\,^\circ\text{C}$ | $21.7\,^\circ\text{C}$ a $24.9\,^\circ\text{C}$ | Modo punto |
| **LED 6** | `D7` | Amarillo | $26.7\,^\circ\text{C}$ | $25.0\,^\circ\text{C}$ a $28.3\,^\circ\text{C}$ | Modo punto |
| **LED 7** | `D8` | Amarillo | $30.0\,^\circ\text{C}$ | $28.4\,^\circ\text{C}$ a $31.6\,^\circ\text{C}$ | Modo punto |
| **LED 8** | `D9` | Naranja | $33.3\,^\circ\text{C}$ | $31.7\,^\circ\text{C}$ a $34.9\,^\circ\text{C}$ | Precaución |
| **LED 9** | `D10` | Naranja | $36.7\,^\circ\text{C}$ | $35.0\,^\circ\text{C}$ a $38.3\,^\circ\text{C}$ | Pre-alarma |
| **LED 10** | `D11` | **Rojo** | **$40.0\,^\circ\text{C}$** | **$\ge 38.4\,^\circ\text{C}$ (incluye $40\,^\circ\text{C}$)** | **Enclava Buzzer + Display `E`** |

---

## 3. Lista Exacta de Materiales (Tinkercad)
1. **1 × Placa Arduino Uno R3**
2. **1 × Placa de pruebas (Protoboard grande)**
3. **1 × Sensor de temperatura TMP36**
4. **10 × LEDs** (sugerido: 4 verdes, 3 amarillos, 2 naranjas, 1 rojo)
5. **10 × Resistencias de $220\,\Omega$** (una para cada LED) + **1 × Resistencia de $220\,\Omega$** en el cátodo común del display de 7 segmentos para protegerlo contra sobrecorriente.
6. **1 × Pulsador (Botón de reinicio / Reset)**
7. **1 × Piezo (Buzzer piezoeléctrico)**
8. **1 × Visualizador de 7 segmentos** — Configurar en Tinkercad como **Cátodo Común**.

---

## 4. Tabla de Conexiones Pin a Pin

### A. Alimentación y Sensor TMP36
*(Mirando la cara plana del TMP36 de frente, con las patas hacia abajo)*
| Pin del TMP36 | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| Pin 1 (Izquierdo — `Potencia`) | `5V` | Riel rojo (`+`) | Rojo |
| Pin 2 (Central — `Vout`) | **A0** | Fila directa a `A0` | Celeste |
| Pin 3 (Derecho — `Tierra`) | `GND` | Riel azul/negro (`-`) | Negro |

### B. Fila de 10 LEDs (Modo Punto)
| Componente | Ánodo (`+`, pata larga) | Cátodo (`-`, pata corta) | Color Sugerido |
| :--- | :---: | :--- | :---: |
| **LED 1** ($10\,^\circ\text{C}$) | **D2** | Resistencia $220\,\Omega$ → Riel `GND` | Verde |
| **LED 2** ($13.3\,^\circ\text{C}$) | **D3** | Resistencia $220\,\Omega$ → Riel `GND` | Verde |
| **LED 3** ($16.7\,^\circ\text{C}$) | **D4** | Resistencia $220\,\Omega$ → Riel `GND` | Verde |
| **LED 4** ($20.0\,^\circ\text{C}$) | **D5** | Resistencia $220\,\Omega$ → Riel `GND` | Verde |
| **LED 5** ($23.3\,^\circ\text{C}$) | **D6** | Resistencia $220\,\Omega$ → Riel `GND` | Amarillo |
| **LED 6** ($26.7\,^\circ\text{C}$) | **D7** | Resistencia $220\,\Omega$ → Riel `GND` | Amarillo |
| **LED 7** ($30.0\,^\circ\text{C}$) | **D8** | Resistencia $220\,\Omega$ → Riel `GND` | Amarillo |
| **LED 8** ($33.3\,^\circ\text{C}$) | **D9** | Resistencia $220\,\Omega$ → Riel `GND` | Naranja |
| **LED 9** ($36.7\,^\circ\text{C}$) | **D10** | Resistencia $220\,\Omega$ → Riel `GND` | Naranja |
| **LED 10** ($40.0\,^\circ\text{C}$) | **D11** | Resistencia $220\,\Omega$ → Riel `GND` | Rojo |

### C. Pulsador de Reinicio (`RESET`) y Buzzer
| Componente y Pin | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| **Pulsador** Terminal 1a | **D12** | Usa `INPUT_PULLUP` interno (no requiere resistencia externa) | Azul |
| **Pulsador** Terminal 2a (lado opuesto) | `GND` | Riel `-` | Negro |
| **Buzzer (Piezo)** Positivo (`+`) | **D13** | Conexión directa | Morado |
| **Buzzer (Piezo)** Negativo (`-`) | `GND` | Riel `-` | Negro |

### D. Display de 7 Segmentos (Cátodo Común) — Letra `E`
*(Solo se conectan los 5 segmentos de la letra `E`: **A, D, E, F, G**; los segmentos **B** y **C** quedan sin conectar).*
| Segmento | Pin Físico del Display | Pin del Arduino Uno | Color Sugerido |
| :---: | :--- | :---: | :---: |
| **A** | Pin 7 (superior, 2.° desde derecha) | **A1** | Rosado |
| **D** | Pin 2 (inferior, 2.° desde izquierda) | **A2** | Rosado |
| **E** | Pin 1 (inferior, extremo izquierdo) | **A3** | Rosado |
| **F** | Pin 9 (superior, 2.° desde izquierda) | **A4** | Rosado |
| **G** | Pin 10 (superior, extremo izquierdo) | **A5** | Rosado |
| **COM** | Pin 3 (central inferior) o Pin 8 (central superior) | `GND` vía resistencia de $220\,\Omega$ | Negro |

---

## 5. Instrucciones Paso a Paso en Tinkercad Circuits
1. Crea un nuevo circuito en Tinkercad y coloca: 1 Arduino Uno R3, 1 Protoboard grande, 1 sensor **TMP36**, 10 LEDs en fila horizontal, 11 resistencias de $220\,\Omega$, 1 pulsador, 1 piezo (buzzer) y 1 visualizador de 7 segmentos.
2. Haz clic sobre el **Visualizador de 7 segmentos** y en su panel de propiedades cambia **Común** a **Cátodo**.
3. Cablea el TMP36, los 10 LEDs (`D2`–`D11`), el pulsador (`D12` a `GND`), el buzzer (`D13` a `GND`) y los segmentos `A, D, E, F, G` del display (`A1`–`A5`) siguiendo la Sección 4.
4. Abre **Código → Texto**, borra el contenido, pega [`sketch.ino`](./sketch.ino) y pulsa **Iniciar simulación**.

### Puntos de Verificación de Funcionamiento
1. Haz clic sobre el sensor **TMP36** para ver su deslizador de temperatura:
   - A **$10\,^\circ\text{C}$**: se enciende **únicamente el LED 1** (todos los demás apagados).
   - A **$25\,^\circ\text{C}$**: se enciende **únicamente el LED 5 o LED 6** (modo punto).
   - Sube la temperatura hasta **$40\,^\circ\text{C}$**: se enciende **únicamente el LED 10**, el **buzzer comienza a sonar** y el **display muestra `E`**.
2. **Prueba de enclavamiento:** Baja la temperatura del TMP36 a **$20\,^\circ\text{C}$** → El punto luminoso vuelve al **LED 4**, pero el **buzzer sigue sonando** y el **display sigue mostrando `E`**.
3. **Prueba de reinicio:** Presiona el **pulsador de RESET** → El buzzer se silencia y el display se apaga inmediatamente.

> **Nota para Wokwi:** El archivo [`diagram.json`](./diagram.json) utiliza un potenciómetro con divisor resistivo (`8.2 kΩ` y `1.1 kΩ`) conectado a `A0` para emular el voltaje analógico del TMP36 ($0.53\text{ V}$ a $1.02\text{ V}$ $\equiv 3\,^\circ\text{C}$ a $52\,^\circ\text{C}$), permitiendo ejecutar el mismo `sketch.ino` sin cambiar una sola línea.
