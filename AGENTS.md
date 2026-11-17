# 🤖 Configuración del Agente de Inteligencia Artificial (Modo Agente IoT)

Este repositorio contiene las prácticas de **Internet de las Cosas (IoT)** de la **Universidad Privada de Tacna (UPT)**.  
**Autores del proyecto:** Fabrizio Salvador Elias Perez Peralta y Gian Franco Arocutipa Arocutipa.

---

## 🎯 Instrucción Maestra para el Agente ("Resuélvelo")

Cuando el usuario pida **"resuelve"**, **"resuélvelo"**, o **suba una guía/documento/imagen de laboratorio** (PDF, DOCX, PNG, JPG):

El agente debe ejecutar de forma **automática, autónoma y rigurosa** el siguiente flujo de trabajo:

---

### 1. Nomenclatura de Carpetas (OBLIGATORIO)
Crea una carpeta nueva con la fecha actual del sistema en la raíz del repositorio:
$$\mathbf{fg\_AAAA-MM-DD}$$
*(Por ejemplo: `fg_2026-11-17`)*.

---

### 2. Archivos Requeridos en la Carpeta
Dentro de la carpeta `fg_YYYY-MM-DD`, genera obligatoriamente estos 3 archivos base:

#### A. `README.md` (Guía Paso a Paso para Tinkercad y Wokwi)
Debe incluir:
1. **Carátula del Laboratorio:** Nombre del ejercicio, autores (Perez Fabrizio y Arocutipa Gian Franco), fecha y resumen del funcionamiento.
2. **Lista Exacta de Materiales (Tinkercad):**
   - Microcontrolador (Arduino Uno R3, Arduino Nano o ESP32).
   - Placa de pruebas (Protoboard).
   - Sensores y actuadores específicos (LEDs, visualizador de 7 segmentos con su tipo exacto: cátodo o ánodo común, sensor ultrasónico, DHT22, etc.).
   - Resistencias con sus valores precisos ($220\,\Omega$, $330\,\Omega$, $1\,\text{k}\Omega$, etc.).
3. **Tabla de Conexiones Pin a Pin:**
   - Mapeo exacto: `Pin del Componente` $\rightarrow$ `Pin del Microcontrolador` $\rightarrow$ `Riel / Fila en Protoboard` $\rightarrow$ `Color sugerido de cable`.
4. **Instrucciones de Simulación en Tinkercad:**
   - Paso a paso para abrir la pestaña **Código $\rightarrow$ Texto** y pegar el sketch.
   - Puntos de verificación de funcionamiento para confirmar que la simulación es 100% correcta.

#### B. `sketch.ino` (Código Fuente Completo de Arduino / ESP32)
- Código en C++/Arduino limpio, completamente funcional y comentado línea por línea.
- Sin librerías inexistentes ni errores de compilación.
- Compatible tanto para el editor de **Tinkercad** como para **Wokwi**.

#### C. `diagram.json` (Esquemático para Wokwi)
- Archivo JSON válido y libre de errores de sintaxis.
- **Regla de oro de pines en Wokwi:**
  - Para **ESP32** (`wokwi-esp32-devkit-v1`): Usar `esp:VIN` (nunca 5V), `esp:D2`, `esp:D5`, `esp:D18`, `esp:D21`, `esp:D22`, `esp:GND.1`, `esp:GND.2`.
  - Para **Arduino Nano** (`wokwi-arduino-nano`): Usar `nano:5V`, `nano:GND.1`, `nano:2` a `nano:13`.
  - Para **Arduino Uno** (`wokwi-arduino-uno`): Usar `uno:5V`, `uno:GND.1`, `uno:7`, `uno:8`, `uno:10`, etc.
  - Para displays de 7 segmentos: `wokwi-7segment` con `"common": "cathode"`.

#### D. `libraries.txt` (Opcional si requiere librerías en Wokwi)
- Si el circuito utiliza librerías (ej. `LiquidCrystal I2C`, `DHT sensor library`, `ThingSpeak`), incluirlas en este archivo.

---

### 3. Sincronización Automática con Git (GitHub)
Una vez generados y validados los archivos:
```bash
git add .
git commit -m "feat: resolver laboratorio en fg_YYYY-MM-DD"
git push origin main
```

---

### 4. Respuesta al Usuario
Al finalizar, responde de forma concisa mostrando:
- El enlace a la carpeta generada: `fg_YYYY-MM-DD`.
- La tabla rápida de conexiones de hardware.
- El código `sketch.ino` listo para copiar.
- La confirmación del push a GitHub.
