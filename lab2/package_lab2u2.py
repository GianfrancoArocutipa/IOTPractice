# -*- coding: utf-8 -*-
import os
import sys
import shutil
import zipfile

def extract_file_content(content, filename, next_files):
    lines = content.splitlines()
    capturing = False
    result = []
    target = f'ARCHIVO: {filename}'
    next_targets = [f'ARCHIVO: {nf}' for nf in next_files]
    for line in lines:
        s = line.strip()
        if not capturing:
            if s == target:
                capturing = True
                continue
        else:
            if s in next_targets or s.startswith('===================='):
                break
            result.append(line)
    
    while result and (result[0].strip().startswith('---') or result[0].strip() == ''):
        result.pop(0)
    while result and (result[-1].strip().startswith('---') or result[-1].strip() == ''):
        result.pop()
    return '\n'.join(result).strip()

def main():

    root_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(root_dir, "lab 2u2")
    os.makedirs(target_dir, exist_ok=True)
    print(f"Target directory: {target_dir}")

    # Read original circuit text files
    with open(os.path.join(root_dir, "02_Circuito1_Contador_0_9_Nano.txt"), "r", encoding="utf-8") as f:
        c1_text = f.read()
    with open(os.path.join(root_dir, "03_Circuito2_Contador_00_99_Multiplexado_Nano.txt"), "r", encoding="utf-8") as f:
        c2_text = f.read()
    with open(os.path.join(root_dir, "04_Circuito3_Sensor_DHT22_Nano.txt"), "r", encoding="utf-8") as f:
        c3_text = f.read()

    # Extract C1 files
    c1_dir = os.path.join(target_dir, "01_Circuito1_Contador_0_9")
    os.makedirs(c1_dir, exist_ok=True)
    c1_sketch = extract_file_content(c1_text, "sketch.ino", ["diagram.json", "2n2222.chip.json"])
    c1_diagram = extract_file_content(c1_text, "diagram.json", ["2n2222.chip.json"])
    with open(os.path.join(c1_dir, "sketch.ino"), "w", encoding="utf-8") as f:
        f.write(c1_sketch)
    with open(os.path.join(c1_dir, "diagram.json"), "w", encoding="utf-8") as f:
        f.write(c1_diagram)
    with open(os.path.join(c1_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Circuito 1: Contador de 0 a 9 con Display de 7 Segmentos (Arduino Nano)

## Descripción
Control de un display de 7 segmentos de cátodo común mostrando el conteo cíclico de 0 a 9.
Adaptado para la configuración con transistores NPN 2N2222:
- Pin D10 en HIGH: Habilita el transistor del display derecho (unidades).
- Pin D9 en LOW: Mantiene apagado el display izquierdo.

## Instrucciones en Wokwi (https://wokwi.com)
1. Pega `sketch.ino` en la pestaña de código.
2. Pega `diagram.json` en la pestaña del diagrama.
3. Presiona Play para ver el conteo de 0 a 9 cada 600 ms.
""")
    print("Circuito 1 extraído con éxito.")

    # Extract C2 files
    c2_dir = os.path.join(target_dir, "02_Circuito2_Contador_00_99_Multiplexado")
    os.makedirs(c2_dir, exist_ok=True)
    c2_sketch = extract_file_content(c2_text, "sketch.ino", ["diagram.json"])
    c2_diagram = extract_file_content(c2_text, "diagram.json", ["2n2222.chip.json"])
    c2_chip_json = extract_file_content(c2_text, "2n2222.chip.json", ["2n2222.chip.c"])
    c2_chip_c = extract_file_content(c2_text, "2n2222.chip.c", [])
    with open(os.path.join(c2_dir, "sketch.ino"), "w", encoding="utf-8") as f:
        f.write(c2_sketch)
    with open(os.path.join(c2_dir, "diagram.json"), "w", encoding="utf-8") as f:
        f.write(c2_diagram)
    with open(os.path.join(c2_dir, "2n2222.chip.json"), "w", encoding="utf-8") as f:
        f.write(c2_chip_json)
    with open(os.path.join(c2_dir, "2n2222.chip.c"), "w", encoding="utf-8") as f:
        f.write(c2_chip_c)
    with open(os.path.join(c2_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Circuito 2: Contador 00 a 99 Multiplexado con Transistores 2N2222 (Arduino Nano)

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
""")
    print("Circuito 2 extraído con éxito.")

    # Extract C3 files
    c3_dir = os.path.join(target_dir, "03_Circuito3_Sensor_DHT22_Multiplexado")
    os.makedirs(c3_dir, exist_ok=True)
    c3_sketch = extract_file_content(c3_text, "sketch.ino", ["diagram.json"])
    c3_diagram = extract_file_content(c3_text, "diagram.json", ["libraries.txt", "2n2222.chip.json"])
    c3_lib = extract_file_content(c3_text, "libraries.txt", ["2n2222.chip.json"])
    c3_chip_json = extract_file_content(c3_text, "2n2222.chip.json", ["2n2222.chip.c"])
    c3_chip_c = extract_file_content(c3_text, "2n2222.chip.c", [])

    with open(os.path.join(c3_dir, "sketch.ino"), "w", encoding="utf-8") as f:
        f.write(c3_sketch)
    with open(os.path.join(c3_dir, "diagram.json"), "w", encoding="utf-8") as f:
        f.write(c3_diagram)
    with open(os.path.join(c3_dir, "libraries.txt"), "w", encoding="utf-8") as f:
        f.write(c3_lib if c3_lib else "DHT sensor library")
    with open(os.path.join(c3_dir, "2n2222.chip.json"), "w", encoding="utf-8") as f:
        f.write(c3_chip_json)
    with open(os.path.join(c3_dir, "2n2222.chip.c"), "w", encoding="utf-8") as f:
        f.write(c3_chip_c)
    with open(os.path.join(c3_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Circuito 3: Sensor DHT22 con Visualización Multiplexada en Displays de 7 Segmentos

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
""")
    print("Circuito 3 extraído con éxito.")

    # Copy Reports
    docx_src = os.path.join(root_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx")
    if not os.path.exists(docx_src):
        docx_src = os.path.join(root_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi.docx")

    # Save multiple well-named copies in target_dir
    shutil.copy2(docx_src, os.path.join(target_dir, "lab 2u2.docx"))
    shutil.copy2(docx_src, os.path.join(target_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx"))
    shutil.copy2(docx_src, os.path.join(target_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2u2 Arduino Nano Wokwi.docx"))
    
    # Also copy to root directory with the direct name 'lab 2u2.docx'
    shutil.copy2(docx_src, os.path.join(root_dir, "lab 2u2.docx"))
    print("Informes Word copiados exitosamente.")

    # Copy PDF guide
    pdf_src = os.path.join(root_dir, "Lab 2.2 Arduino Nano Wokwi.pdf")
    if os.path.exists(pdf_src):
        shutil.copy2(pdf_src, os.path.join(target_dir, "Lab 2.2 Arduino Nano Wokwi.pdf"))
        shutil.copy2(pdf_src, os.path.join(target_dir, "Guia_Docente_Lab_2.2_Arduino_Nano.pdf"))
        print("Guía docente PDF copiada.")

    # Copy TODOS_LOS_EJERCICIOS_WOKWI.txt
    master_txt = os.path.join(root_dir, "TODOS_LOS_EJERCICIOS_WOKWI.txt")
    if os.path.exists(master_txt):
        shutil.copy2(master_txt, os.path.join(target_dir, "TODOS_LOS_EJERCICIOS_WOKWI.txt"))

    # Copy script and assets
    scripts_dir = os.path.join(target_dir, "scripts_informe")
    os.makedirs(scripts_dir, exist_ok=True)
    shutil.copy2(os.path.join(root_dir, "generate_final_report.py"), os.path.join(scripts_dir, "generate_final_report.py"))
    
    # Copy extracted assets
    assets_src = os.path.join(root_dir, "extracted_assets")
    assets_dst = os.path.join(scripts_dir, "extracted_assets")
    if os.path.exists(assets_src):
        if os.path.exists(assets_dst):
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
        # Also copy extracted_assets to target_dir so report generation can run directly inside lab 2u2
        target_assets = os.path.join(target_dir, "extracted_assets")
        if os.path.exists(target_assets):
            shutil.rmtree(target_assets)
        shutil.copytree(assets_src, target_assets)
        print("Assets y logos copiados.")

    # Copy original text notes
    notes_dir = os.path.join(target_dir, "archivos_texto_originales")
    os.makedirs(notes_dir, exist_ok=True)
    shutil.copy2(os.path.join(root_dir, "02_Circuito1_Contador_0_9_Nano.txt"), os.path.join(notes_dir, "02_Circuito1_Contador_0_9_Nano.txt"))
    shutil.copy2(os.path.join(root_dir, "03_Circuito2_Contador_00_99_Multiplexado_Nano.txt"), os.path.join(notes_dir, "03_Circuito2_Contador_00_99_Multiplexado_Nano.txt"))
    shutil.copy2(os.path.join(root_dir, "04_Circuito3_Sensor_DHT22_Nano.txt"), os.path.join(notes_dir, "04_Circuito3_Sensor_DHT22_Nano.txt"))

    # Create root README for 'lab 2u2'
    readme_content = """# Laboratorio 2 - Unidad 2 (Lab 2U2): Arduino Nano, Displays 7 Segmentos, Multiplexación y DHT22

**Universidad Privada de Tacna**  
**Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas  
**Docente:** Mgr. Alex Juan Yanqui Constancio  

**Integrantes:**
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790

---

## Estructura de la Carpeta `lab 2u2`

Esta carpeta contiene la totalidad de los entregables, códigos funcionales de simulación en Wokwi, guías y el informe académico formal:

```
lab 2u2/
│
├── lab 2u2.docx                                                   # Informe final completo en formato Word
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2u2 Arduino Nano Wokwi.docx
├── Lab 2.2 Arduino Nano Wokwi.pdf                                 # Guía oficial del docente
├── TODOS_LOS_EJERCICIOS_WOKWI.txt                                 # Archivo unificado de códigos y esquemas Wokwi
│
├── 01_Circuito1_Contador_0_9/                                     # Circuito 1: Contador 0 a 9 en 1 Display
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 02_Circuito2_Contador_00_99_Multiplexado/                      # Circuito 2: Contador 00 a 99 multiplexado
│   ├── sketch.ino
│   ├── diagram.json
│   ├── 2n2222.chip.json                                           # Definición del Custom Chip 2N2222
│   ├── 2n2222.chip.c                                              # Lógica de conmutación en lenguaje C
│   └── README.md
│
├── 03_Circuito3_Sensor_DHT22_Multiplexado/                        # Circuito 3: Sensor DHT22 + Multiplexación
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   ├── 2n2222.chip.json
│   ├── 2n2222.chip.c
│   └── README.md
│
├── scripts_informe/                                               # Script generador en Python y plantillas
│   ├── generate_final_report.py
│   └── extracted_assets/
│
└── archivos_texto_originales/                                     # Registros y anotaciones de depuración
    ├── 02_Circuito1_Contador_0_9_Nano.txt
    ├── 03_Circuito2_Contador_00_99_Multiplexado_Nano.txt
    └── 04_Circuito3_Sensor_DHT22_Nano.txt
```

---

## Resumen Técnico de los Circuitos

1. **Circuito 1: Contador de 0 a 9**
   - Manejo del display de 7 segmentos de cátodo común mediante los pines D2 a D8.
   - Activación controlada del transistor derecho (Pin D10 = HIGH) para permitir conteo limpio en una sola pantalla.

2. **Circuito 2: Contador 00 a 99 Multiplexado**
   - Conmutación rápida (~125 Hz) de dos displays mediante transistores NPN 2N2222 gobernados por los pines D9 (decenas) y D10 (unidades).
   - Aprovechamiento del fenómeno POV (Persistencia de la Visión) para lograr visión simultánea libre de parpadeo.
   - Solución del error de cortocircuito a GND retirando los puentes redundantes.

3. **Circuito 3: Sensor Digital DHT22 con Visualización en Displays**
   - Lectura digital unifilar de temperatura y humedad ambiental (Pin D11).
   - Conversión de grados Celsius a dígitos individuales (decenas y unidades).
   - Despliegue en tiempo real en los displays de 7 segmentos y monitoreo continuo por puerto serial a 9600 baudios.
"""
    with open(os.path.join(target_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("README.md creado.")

    # Create ZIP archive 'lab 2u2.zip'
    zip_in_target = os.path.join(target_dir, "lab 2u2.zip")
    if os.path.exists(zip_in_target):
        os.remove(zip_in_target)

    zip_path = os.path.join(root_dir, "lab 2u2.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"Creating ZIP archive at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".zip"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                zipf.write(full_path, rel_path)
    
    print("Archivo 'lab 2u2.zip' generado con éxito.")

if __name__ == "__main__":
    main()

