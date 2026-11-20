# Ejercicio 1 — Sensor de Medición de Nivel y Volumen en Dos Tanques con Control de Válvula

## 1. Carátula del Laboratorio
- **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
- **Curso:** Internet de las Cosas (IoT) — Examen de Unidad 2 (Ciclo 2026 - II)
- **Docente:** Ing. Alex Yanqui Constancio
- **Autores:** Fabrizio Salvador Elias Perez Peralta y Gian Franco Arocutipa Arocutipa
- **Fecha:** 2026-11-20
- **Resumen del funcionamiento:** Sistema basado en Arduino Uno que mide en tiempo real la altura de líquido ($h_1$ y $h_2$) y calcula el volumen en litros de **dos tanques cilíndricos** de $2\text{ m}$ de alto y $0.5\text{ m}$ de radio ($V_{\text{máx}} \approx 1570.8\text{ L}$ cada uno) mediante dos sensores ultrasónicos **HC-SR04**. Muestra en una pantalla **LCD 16×2** el volumen y porcentaje de ambos tanques; cuando el nivel alcanza el **90%** se enciende un **LED rojo de alarma**, y al superar el **95%** un **servomotor** gira a $0^\circ$ simulando el cierre automático de la válvula de entrada $q_i$.

---

## 2. Análisis Matemático de los Tanques
Cada tanque es un cilindro vertical con:
- Altura total: $H = 2.0\text{ m} = 200\text{ cm}$
- Radio: $R = 0.5\text{ m}$
- Área de la base: $A = \pi \cdot R^2 = \pi \cdot (0.5)^2 \approx 0.7854\text{ m}^2$
- Volumen máximo por tanque:
$$V_{\text{máx}} = \pi \cdot R^2 \cdot H = 0.7854 \times 2.0 = 1.5708\text{ m}^3 = 1570.8\text{ L}$$
- Altura del líquido a partir de la distancia $d$ medida por el HC-SR04 desde la tapa superior:
$$h = 200 - d \quad (\text{limitado entre } 0\text{ y }200\text{ cm})$$
- Volumen instantáneo en litros y porcentaje:
$$V(\text{L}) = \pi \cdot (0.5)^2 \cdot \frac{h}{100} \cdot 1000 \approx 7.854 \cdot h$$
$$\%\,\text{Nivel} = \frac{V}{V_{\text{máx}}} \times 100 = \frac{h}{200} \times 100$$

| Nivel del Tanque | Distancia HC-SR04 ($d$) | Altura Líquido ($h$) | Volumen ($V$) | LED Alarma | Válvula (Servo) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0% (Vacío) | $\ge 200\text{ cm}$ | $0\text{ cm}$ | $0\text{ L}$ | Apagado | Abierta ($90^\circ$) |
| 50% (Medio) | $100\text{ cm}$ | $100\text{ cm}$ | $785\text{ L}$ | Apagado | Abierta ($90^\circ$) |
| **90% (Alarma)** | **$20\text{ cm}$** | **$180\text{ cm}$** | **$1414\text{ L}$** | **ENCENDIDO** | Abierta ($90^\circ$) |
| **> 95% (Cierre)** | **$< 10\text{ cm}$** | **$> 190\text{ cm}$** | **$> 1492\text{ L}$** | **ENCENDIDO** | **CERRADA ($0^\circ$)** |
| 100% (Lleno) | $\le 2\text{ cm}$ | $198\text{--}200\text{ cm}$ | $1555\text{--}1571\text{ L}$ | ENCENDIDO | CERRADA ($0^\circ$) |

---

## 3. Lista Exacta de Materiales (Tinkercad)
1. **1 × Placa Arduino Uno R3**
2. **1 × Placa de pruebas (Protoboard grande o mediana)**
3. **2 × Sensores de distancia ultrasónicos HC-SR04** (de 4 pines: `VCC`, `TRIG`, `ECHO`, `GND`) — uno para Tanque 1 ($h_1$) y otro para Tanque 2 ($h_2$).
4. **1 × Pantalla LCD 16 × 2** (paralela estándar de 16 pines).
5. **1 × Potenciómetro de $10\,\text{k}\Omega$** (para regular el contraste `V0` del LCD).
6. **1 × Micro Servomotor** (simula la válvula motorizada de entrada $q_i$).
7. **1 × LED Rojo** (indicador de alarma al 90%).
8. **2 × Resistencias de $220\,\Omega$** (1 para la luz de fondo `LED+` del LCD y 1 para el LED de alarma).

---

## 4. Tabla de Conexiones Pin a Pin

### A. Alimentación General en Protoboard
| Origen (Arduino Uno) | Destino (Protoboard) | Color de Cable Sugerido |
| :--- | :--- | :---: |
| `5V` | Riel positivo rojo (`+`) superior e inferior | Rojo |
| `GND` | Riel negativo azul/negro (`-`) superior e inferior | Negro |

### B. Pantalla LCD 16×2 y Potenciómetro de Contraste
| Pin del LCD 16×2 | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| `GND` (`VSS`) | `GND` | Riel `-` | Negro |
| `VCC` (`VDD`) | `5V` | Riel `+` | Rojo |
| `V0` (Contraste) | — | Pin central (`Wiper`) del Potenciómetro $10\,\text{k}\Omega$ (extremos del pot a `+` y `-`) | Celeste |
| `RS` | **D12** | Fila directa a `RS` | Naranja |
| `RW` | `GND` | Riel `-` (solo escritura) | Negro |
| `E` (`Enable`) | **D11** | Fila directa a `E` | Amarillo |
| `DB4` | **D5** | Fila directa a `DB4` | Verde |
| `DB5` | **D4** | Fila directa a `DB5` | Azul |
| `DB6` | **D3** | Fila directa a `DB6` | Morado |
| `DB7` | **D2** | Fila directa a `DB7` | Rosado |
| `LED+` (`A`) | `5V` | A través de resistencia de $220\,\Omega$ al riel `+` | Rojo |
| `LED-` (`K`) | `GND` | Riel `-` | Negro |

### C. Sensores Ultrasónicos HC-SR04 (Tanque 1 y Tanque 2)
| Componente y Pin | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| **HC-SR04 #1 (Tanque 1)** `VCC` | `5V` | Riel `+` | Rojo |
| **HC-SR04 #1 (Tanque 1)** `TRIG` | **D6** | Fila directa | Marrón |
| **HC-SR04 #1 (Tanque 1)** `ECHO` | **D7** | Fila directa | Verde claro |
| **HC-SR04 #1 (Tanque 1)** `GND` | `GND` | Riel `-` | Negro |
| **HC-SR04 #2 (Tanque 2)** `VCC` | `5V` | Riel `+` | Rojo |
| **HC-SR04 #2 (Tanque 2)** `TRIG` | **D8** | Fila directa | Dorado / Amarillo |
| **HC-SR04 #2 (Tanque 2)** `ECHO` | **D9** | Fila directa | Turquesa |
| **HC-SR04 #2 (Tanque 2)** `GND` | `GND` | Riel `-` | Negro |

### D. Servomotor (Válvula) y LED de Alarma
| Componente y Pin | Pin del Arduino Uno | Riel / Fila en Protoboard | Color Sugerido |
| :--- | :---: | :--- | :---: |
| **Micro Servo** `Potencia` (cable rojo) | `5V` | Riel `+` | Rojo |
| **Micro Servo** `Tierra` (cable marrón/negro) | `GND` | Riel `-` | Negro |
| **Micro Servo** `Señal` (cable naranja) | **D10** | Conexión directa | Naranja |
| **LED Rojo** Ánodo (`+`, pata larga) | **D13** | Fila directa | Rojo |
| **LED Rojo** Cátodo (`-`, pata corta) | `GND` | A través de resistencia de $220\,\Omega$ al riel `-` | Negro |

---

## 5. Instrucciones Paso a Paso en Tinkercad Circuits
1. Ingresa a [Tinkercad](https://www.tinkercad.com/) → **Diseños** → **Crear** → **Circuito**.
2. En el buscador de componentes (panel derecho), cambia el filtro de **Básico** a **Todos** para encontrar el sensor **HC-SR04** (de 4 pines, no el PING de 3 pines).
3. Arrastra al área de trabajo: 1 Arduino Uno R3, 1 Protoboard, 1 LCD 16×2, 1 Potenciómetro ($10\,\text{k}\Omega$), 2 HC-SR04, 1 Micro Servomotor, 1 LED rojo y 2 resistencias de $220\,\Omega$.
4. Realiza el cableado siguiendo exactamente las tablas de la Sección 4.
5. Haz clic en **Código** (arriba a la derecha), cambia de **Bloques** a **Texto** y confirma **Continuar**.
6. Borra el código de ejemplo, pega el contenido completo de [`sketch.ino`](./sketch.ino) y pulsa **Iniciar simulación**.
7. **Ajuste de contraste del LCD:** Si la pantalla enciende pero no ves letras, gira la perilla del potenciómetro hacia un extremo (cerca de GND) hasta que aparezca el texto `T1:...` y `T2:...`.

### Puntos de Verificación de Funcionamiento
- Haz clic sobre el **HC-SR04 #1** durante la simulación para abrir su deslizador de distancia:
  1. Ubica el objeto a **100 cm** → El LCD muestra `T1: 785L  50% AB`, LED apagado, Servo en $90^\circ$ (Abierta).
  2. Acerca el objeto a **18 cm** ($\approx 91\%$) → El LCD muestra `AL`, el **LED rojo se enciende**, la válvula sigue en `AB` ($90^\circ$).
  3. Acerca el objeto a **6 cm** ($\approx 97\%$) → El LCD muestra `CE` y `AL`, el **LED rojo permanece encendido** y el **Servomotor gira a $0^\circ$** cerrando la válvula de entrada.
  4. Repite la prueba con el **HC-SR04 #2** para verificar el monitoreo simultáneo del Tanque 2.
