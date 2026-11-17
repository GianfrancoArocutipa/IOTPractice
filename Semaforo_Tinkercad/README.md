# Semáforo Inteligente con Display de 7 Segmentos (Guía Tinkercad & Wokwi)

Este proyecto corresponde a la reconstrucción completa del archivo `Semaforo.brd` exportado desde Autodesk Tinkercad / EAGLE.

---

## ❓ ¿Se puede cargar el archivo `.brd` directamente en Tinkercad?

**Respuesta rápida:** **NO, no se puede.**

### ¿Por qué?
1. **El archivo `.brd` es un archivo de PCB (placa de circuito impreso para manufactura en Autodesk EAGLE).**  
   Tinkercad Circuits permite **exportar** a `.brd` para enviar a fabricar la placa física, pero **NO tiene la función de importar un archivo `.brd`** para reconstruir los componentes 3D y cables interactivos en pantalla.
2. **La opción "Importar" de Tinkercad solo sirve para Modelos 3D** (archivos `.stl`, `.obj`, `.svg`). En la sección **Circuitos**, solo se puede importar el **archivo de código `.ino`** en el editor de texto.
3. **¿Cómo se comparten circuitos en Tinkercad?**  
   Si otra persona te va a pasar un circuito ya hecho, debe pasarte el **Enlace de Compartir de Tinkercad**:
   - En Tinkercad: Botón **"Compartir"** $\rightarrow$ **"Invitar a personas"** $\rightarrow$ **"Copiar enlace"**.
   - Con ese enlace, tú entras desde tu navegador y le das clic a **"Copiar y aplicar cambios" (Copy & Tinker)**. Eso te clona el circuito completo en tu cuenta en 1 segundo.

---

## 🛠️ Paso a Paso para Armarlo en Tinkercad Circuits

Si debes armarlo tú mismo en Tinkercad, sigue estos sencillos pasos:

### 1. Lista de Componentes a Arrastrar (Panel Derecho)
- 1 × **Placa Arduino Uno R3**
- 1 × **Placa de pruebas pequeña (Protoboard)**
- 1 × **Visualizador de 7 segmentos** (Asegúrate de configurarlo en su menú desplegable como **Cátodo Común**)
- 1 × **LED Rojo**
- 1 × **LED Amarillo**
- 1 × **LED Verde**
- 10 × **Resistencias de $220\,\Omega$** (o $330\,\Omega$ / $1\,\text{k}\Omega$):
  - 3 para los LEDs.
  - 7 para los segmentos del display.

---

### 2. Tabla de Conexiones Exactas

#### A. Conexión de Alimentación y Tierra
- Pin **GND** de Arduino $\rightarrow$ Riel azul/negro (`-`) de la Protoboard.
- Pin **5V** de Arduino $\rightarrow$ Riel rojo (`+`) de la Protoboard.

#### B. Semáforo (LEDs)
| LED | Color | Ánodo (+) | Cátodo (-) |
| :--- | :--- | :--- | :--- |
| **D3** | Rojo | **Pin digital 7** de Arduino | A través de resistencia de $220\,\Omega$ al riel **GND** |
| **D1** | Amarillo | **Pin digital 8** de Arduino | A través de resistencia de $220\,\Omega$ al riel **GND** |
| **D2** | Verde | **Pin digital 10** de Arduino | A través de resistencia de $220\,\Omega$ al riel **GND** |

#### C. Display de 7 Segmentos (Cátodo Común)
El display de 7 segmentos tiene 10 pines (5 arriba y 5 abajo):
- **Pines COM (Tierra común):** El pin central inferior (Pin 3) y el pin central superior (Pin 8) van al riel **GND**.
- **Pines de los Segmentos:** Cada uno se conecta desde el Arduino con una resistencia de $220\,\Omega$:

| Segmento | Pin del Display | Pin Arduino Uno |
| :---: | :---: | :---: |
| **A** | Pin 7 (superior) | **Pin digital 13** |
| **B** | Pin 6 (superior) | **Pin digital 12** |
| **C** | Pin 4 (inferior) | **Pin digital 11** |
| **D** | Pin 2 (inferior) | **Pin digital 9** |
| **E** | Pin 1 (inferior) | **Pin digital 6** |
| **F** | Pin 9 (superior) | **Pin digital 5** |
| **G** | Pin 10 (superior) | **Pin digital 4** |

---

### 3. Cargar el Código en Tinkercad
1. En la barra superior de Tinkercad, haz clic en el botón **"Código"**.
2. Cambia el desplegable de **"Bloques"** a **"Texto"** (confirma el mensaje de aviso).
3. Borra el código por defecto y pega el siguiente código:

```cpp
// ==================== PINES DE LOS LEDS DEL SEMÁFORO ====================
const int LED_ROJO     = 7;   // D7 en Arduino Uno
const int LED_AMARILLO = 8;   // D8 en Arduino Uno
const int LED_VERDE    = 10;  // D10 en Arduino Uno

// ==================== PINES DEL DISPLAY DE 7 SEGMENTOS ====================
const int SEG_A = 13;  // D13 -> Segmento A
const int SEG_B = 12;  // D12 -> Segmento B
const int SEG_C = 11;  // D11 -> Segmento C
const int SEG_D = 9;   // D9  -> Segmento D
const int SEG_E = 6;   // D6  -> Segmento E
const int SEG_F = 5;   // D5  -> Segmento F
const int SEG_G = 4;   // D4  -> Segmento G

// Tabla de segmentos para Cátodo Común (1 = Encendido, 0 = Apagado)
const byte numeros[10][7] = {
  {1, 1, 1, 1, 1, 1, 0}, // 0
  {0, 1, 1, 0, 0, 0, 0}, // 1
  {1, 1, 0, 1, 1, 0, 1}, // 2
  {1, 1, 1, 1, 0, 0, 1}, // 3
  {0, 1, 1, 0, 0, 1, 1}, // 4
  {1, 0, 1, 1, 0, 1, 1}, // 5
  {1, 0, 1, 1, 1, 1, 1}, // 6
  {1, 1, 1, 0, 0, 0, 0}, // 7
  {1, 1, 1, 1, 1, 1, 1}, // 8
  {1, 1, 1, 1, 0, 1, 1}  // 9
};

void setup() {
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  pinMode(SEG_A, OUTPUT);
  pinMode(SEG_B, OUTPUT);
  pinMode(SEG_C, OUTPUT);
  pinMode(SEG_D, OUTPUT);
  pinMode(SEG_E, OUTPUT);
  pinMode(SEG_F, OUTPUT);
  pinMode(SEG_G, OUTPUT);

  apagarLeds();
  apagarDisplay();
}

void mostrarNumero(int num) {
  if (num < 0 || num > 9) return;
  digitalWrite(SEG_A, numeros[num][0]);
  digitalWrite(SEG_B, numeros[num][1]);
  digitalWrite(SEG_C, numeros[num][2]);
  digitalWrite(SEG_D, numeros[num][3]);
  digitalWrite(SEG_E, numeros[num][4]);
  digitalWrite(SEG_F, numeros[num][5]);
  digitalWrite(SEG_G, numeros[num][6]);
}

void apagarDisplay() {
  digitalWrite(SEG_A, LOW);
  digitalWrite(SEG_B, LOW);
  digitalWrite(SEG_C, LOW);
  digitalWrite(SEG_D, LOW);
  digitalWrite(SEG_E, LOW);
  digitalWrite(SEG_F, LOW);
  digitalWrite(SEG_G, LOW);
}

void apagarLeds() {
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);
}

void loop() {
  // --- 1. FASE VERDE: Paso vehicular con cuenta regresiva del 5 al 1 ---
  apagarLeds();
  digitalWrite(LED_VERDE, HIGH);
  for (int i = 5; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }

  // --- 2. FASE AMARILLA: Precaución durante 2 segundos ---
  apagarLeds();
  digitalWrite(LED_AMARILLO, HIGH);
  for (int i = 2; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }

  // --- 3. FASE ROJA: Detención con cuenta regresiva del 5 al 1 ---
  apagarLeds();
  digitalWrite(LED_ROJO, HIGH);
  for (int i = 5; i >= 1; i--) {
    mostrarNumero(i);
    delay(1000);
  }
}
```

4. Haz clic en **"Iniciar simulación"** y verás cómo funciona de inmediato.
