# Ejercicio 3 — Sistema de Estacionamiento con HC-SR04, 3 Displays de 7 Segmentos (0–330 cm), LEDs y Alarma

## 1. Carátula del Laboratorio
- **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
- **Curso:** Internet de las Cosas (IoT) — Examen de Unidad 2 (Ciclo 2026 - II)
- **Docente:** Ing. Alex Yanqui Constancio
- **Autores:** Fabrizio Salvador Elias Perez Peralta y Gian Franco Arocutipa Arocutipa
- **Fecha:** 2026-11-20
- **Resumen del funcionamiento:** Asistente de estacionamiento vehicular basado en Arduino Uno y sensor ultrasónico **HC-SR04** que mide la distancia en centímetros (**0 a 330 cm**) y la muestra en **3 displays de 7 segmentos** (cátodo común) multiplexados sin parpadeo mediante **Persistencia de la Visión (POV)**. Según la proximidad del obstáculo, activa un **LED verde parpadeando** ($> 3.0\text{ m}$), un **LED naranja fijo** ($1.0\text{ m}$ a $3.0\text{ m}$), o un **LED rojo fijo junto con una alarma sonora** ($< 1.0\text{ m}$).

---

## 2. Lógica de Zonas de Estacionamiento

| Zona | Distancia en Metros | Distancia en cm | Displays 7 Seg. | LED Verde | LED Naranja | LED Rojo | Buzzer (Alarma) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Segura** | $> 3.0\text{ m}$ | $301\text{--}330\text{ cm}$ | `301` a `330` | **Parpadeando** (300 ms) | Apagado | Apagado | Silencio |
| **Precaución** | $1.0\text{ m}$ a $3.0\text{ m}$ | $100\text{--}300\text{ cm}$ | `100` a `300` | Apagado | **Encendido fijo** | Apagado | Silencio |
| **Peligro** | $< 1.0\text{ m}$ | $0\text{--}99\text{ cm}$ | `000` a `099` | Apagado | Apagado | **Encendido fijo** | **SONANDO** ($1200\text{ Hz}$) |

---

## 3. Lista Exacta de Materiales (Tinkercad)
1. **1 × Placa Arduino Uno R3**
2. **1 × Placa de pruebas (Protoboard grande)**
3. **1 × Sensor de distancia ultrasónico HC-SR04** (4 pines: `VCC`, `TRIG`, `ECHO`, `GND`)
4. **3 × Visualizadores de 7 segmentos** — Configurar los tres en **Cátodo Común**
5. **7 × Resistencias de $560\,\Omega$** (una en cada línea compartida de segmento `A`–`G`, limita la corriente total por cátodo a $\le 40\text{ mA}$ incluso mostrando `888`)
6. **3 × LEDs:** 1 Verde, 1 Naranja, 1 Rojo
7. **3 × Resistencias de $220\,\Omega$** (una para cada LED indicador)
8. **1 × Piezo (Buzzer piezoeléctrico)**

---

## 4. Tabla de Conexiones Pin a Pin

### A. Bus Compartido de Segmentos (a los 3 Displays de 7 Segmentos)
*(Conecta cada pin del Arduino a través de su resistencia de $560\,\Omega$ hacia el segmento correspondiente del Display 1, y puentea ese mismo segmento del Display 1 al Display 2 y del Display 2 al Display 3).*

| Segmento | Pin Físico en cada Display | Pin Arduino Uno | Resistencia en Serie | Color Sugerido |
| :---: | :--- | :---: | :---: | :---: |
| **A** | Pin 7 (superior, 2.° desde derecha) | **D2** | $560\,\Omega$ | Morado |
| **B** | Pin 6 (superior, extremo derecho) | **D3** | $560\,\Omega$ | Azul |
| **C** | Pin 4 (inferior, 2.° desde derecha) | **D4** | $560\,\Omega$ | Celeste |
| **D** | Pin 2 (inferior, 2.° desde izquierda) | **D5** | $560\,\Omega$ | Verde |
| **E** | Pin 1 (inferior, extremo izquierdo) | **D6** | $560\,\Omega$ | Amarillo |
| **F** | Pin 9 (superior, 2.° desde izquierda) | **D7** | $560\,\Omega$ | Naranja |
| **G** | Pin 10 (superior, extremo izquierdo) | **D8** | $560\,\Omega$ | Rosado |

### B. Selección de Dígito (Cátodos Comunes — Multiplexación)
| Display | Posición | Pin `COM` (Pin 3 inferior o Pin 8 superior) | Pin Arduino Uno | Color Sugerido |
| :--- | :--- | :--- | :---: | :---: |
| **Display 1** | **Centenas** (Izquierda) | `COM` directo (sin conectar a GND) | **D9** | Blanco |
| **Display 2** | **Decenas** (Centro) | `COM` directo (sin conectar a GND) | **D10** | Gris |
| **Display 3** | **Unidades** (Derecha) | `COM` directo (sin conectar a GND) | **D11** | Marrón |

### C. Sensor Ultrasónico HC-SR04
| Pin del HC-SR04 | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| `VCC` | `5V` | Riel rojo (`+`) | Rojo |
| `TRIG` | **D12** | Conexión directa | Dorado / Amarillo |
| `ECHO` | **D13** | Conexión directa | Verde claro |
| `GND` | `GND` | Riel azul/negro (`-`) | Negro |

### D. LEDs Indicadores y Buzzer (Alarma)
| Componente y Pin | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| **LED Verde** Ánodo (`+`) | **A0** | Cátodo (`-`) → $220\,\Omega$ → Riel `GND` | Verde |
| **LED Naranja** Ánodo (`+`) | **A1** | Cátodo (`-`) → $220\,\Omega$ → Riel `GND` | Naranja |
| **LED Rojo** Ánodo (`+`) | **A2** | Cátodo (`-`) → $220\,\Omega$ → Riel `GND` | Rojo |
| **Buzzer (Piezo)** Positivo (`+`) | **A3** | Negativo (`-`) → Riel `GND` | Morado |

---

## 5. Instrucciones Paso a Paso en Tinkercad Circuits
1. Crea un nuevo circuito en Tinkercad y arrastra: 1 Arduino Uno R3, 1 Protoboard grande, 3 Visualizadores de 7 segmentos, 1 sensor **HC-SR04** (de 4 pines, seleccionando **Todos** en componentes), 3 LEDs (Verde, Naranja, Rojo), 1 Piezo, 7 resistencias de $560\,\Omega$ y 3 resistencias de $220\,\Omega$.
2. Haz clic en cada uno de los **3 visualizadores de 7 segmentos** y verifica que los tres estén configurados en **Cátodo Común**.
3. Coloca los 3 displays alineados horizontalmente cruzando el canal central de la protoboard (Izquierda = Centenas, Centro = Decenas, Derecha = Unidades).
4. Conecta los puentes de segmentos `A`–`G` entre los tres displays (A con A, B con B, ..., G con G) y alimenta cada bus desde `D2`–`D8` mediante su resistencia de $560\,\Omega$.
5. Conecta los pines `COM` de cada display **por separado** a `D9` (Centenas), `D10` (Decenas) y `D11` (Unidades). **Importante:** los pines `COM` NO van a `GND` porque el Arduino los conmuta electrónicamente.
6. Cablea el HC-SR04 (`D12`, `D13`), los 3 LEDs (`A0`, `A1`, `A2`) y el Buzzer (`A3`) siguiendo la Sección 4.
7. Abre **Código → Texto**, pega [`sketch.ino`](./sketch.ino) y pulsa **Iniciar simulación**.

### Puntos de Verificación de Funcionamiento
Haz clic sobre el sensor **HC-SR04** en simulación y desplaza el punto objetivo:
1. **315 cm ($> 3.0\text{ m}$):** Los 3 displays muestran **`3 1 5`**, el **LED verde parpadea** constantemente y el buzzer está en silencio.
2. **125 cm ($1.0\text{ m}$ a $3.0\text{ m}$):** Los 3 displays muestran **`1 2 5`**, el **LED naranja** permanece encendido fijo y el buzzer está en silencio.
3. **55 cm ($< 1.0\text{ m}$):** Los 3 displays muestran **`0 5 5`**, el **LED rojo** permanece encendido fijo y la **alarma sonora suena continuamente**.
