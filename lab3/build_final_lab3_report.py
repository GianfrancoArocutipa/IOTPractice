# -*- coding: utf-8 -*-
"""
Report generator script for Lab 3 (Lab 2.3 - Esp32 Wokwi - Adafruit IO):
Exact replica of format, structure, color palette, and styles from Lab 2 report (generate_final_report.py):
- All text in black (RGB 0,0,0) and Arial 11pt, 1.15 line spacing
- Headings in bold black Arial 11pt
- Same gray code boxes (background D9D9D9, border B0B0B0, Consolas 9pt)
- Same capture placeholders (background F4F6F9, dashed border 2E5B82, blue header, green checkmarks)
- Same table styles, headers, and borders
- Same UPT header (with logo) and footer (with page number and teacher name)
- Wokwi simulation files and packaging into 'lab 3u2'

Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas
Curso: Internet de las Cosas
Docente: Mgr. Alex Juan Yanqui Constancio
Estudiantes:
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790
"""

import os
import sys
import json
import shutil
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="000000", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def setup_page_layout(doc, assets_dir):
    for s in doc.sections:
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.0)
        s.different_first_page_header_footer = True

        # Header (Pages 2+)
        header = s.header
        header_tbl = header.add_table(rows=1, cols=2, width=Inches(6.25))
        header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        cell_l = header_tbl.rows[0].cells[0]
        cell_l.width = Inches(0.8)
        set_cell_borders(cell_l, bottom="single", color="000000", sz="6")
        set_cell_margins(cell_l, top=0, bottom=60, left=0, right=0)
        p_img = cell_l.paragraphs[0]
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(2)
        h_logo = os.path.join(assets_dir, 'header_logo_18.png')
        if os.path.exists(h_logo):
            p_img.add_run().add_picture(h_logo, width=Inches(0.35))
        
        cell_r = header_tbl.rows[0].cells[1]
        cell_r.width = Inches(5.45)
        set_cell_borders(cell_r, bottom="single", color="000000", sz="6")
        set_cell_margins(cell_r, top=0, bottom=60, left=0, right=0)
        p_txt = cell_r.paragraphs[0]
        p_txt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_txt.paragraph_format.space_before = Pt(6)
        p_txt.paragraph_format.space_after = Pt(2)
        r = p_txt.add_run('Escuela Profesional de Ingeniería de Sistemas')
        r.font.name = 'Arial'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0, 0, 0)

        # Footer (Pages 2+)
        footer = s.footer
        footer_tbl = footer.add_table(rows=1, cols=2, width=Inches(6.25))
        footer_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        f_cell_l = footer_tbl.rows[0].cells[0]
        f_cell_l.width = Inches(2.5)
        set_cell_borders(f_cell_l, top="single", color="000000", sz="6")
        set_cell_margins(f_cell_l, top=80, bottom=0, left=0, right=0)
        p_pg = f_cell_l.paragraphs[0]
        p_pg.paragraph_format.space_before = Pt(4)
        p_pg.paragraph_format.space_after = Pt(0)
        p_pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        r1 = p_pg.add_run('- ')
        r1.font.name = 'Arial'
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0, 0, 0)
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        p_pg._p.append(fldSimple)
        r2 = p_pg.add_run(' -')
        r2.font.name = 'Arial'
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0, 0, 0)

        f_cell_r = footer_tbl.rows[0].cells[1]
        f_cell_r.width = Inches(3.75)
        set_cell_borders(f_cell_r, top="single", color="000000", sz="6")
        set_cell_margins(f_cell_r, top=80, bottom=0, left=0, right=0)
        p_tea = f_cell_r.paragraphs[0]
        p_tea.paragraph_format.space_before = Pt(4)
        p_tea.paragraph_format.space_after = Pt(0)
        p_tea.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_tea = p_tea.add_run('Mgr. Alex Juan Yanqui Constancio')
        r_tea.font.name = 'Arial'
        r_tea.font.size = Pt(10)
        r_tea.font.color.rgb = RGBColor(0, 0, 0)

def add_p(doc, text="", space_before=0, space_after=5, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, font_size=11, color_rgb=(0,0,0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(*color_rgb)
    return p

def add_bullet(doc, text, bold_prefix="", space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    r_sym = p.add_run("•  ")
    r_sym.font.name = 'Arial'
    r_sym.font.size = Pt(11)
    r_sym.font.bold = True
    r_sym.font.color.rgb = RGBColor(0, 0, 0)

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)

    r_txt = p.add_run(text)
    r_txt.font.name = 'Arial'
    r_txt.font.size = Pt(11)
    r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_num_item(doc, num_str, text, bold_title="", space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    r_num = p.add_run(f"{num_str}. ")
    r_num.font.name = 'Arial'
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)

    if bold_title:
        r_bt = p.add_run(bold_title + ": ")
        r_bt.font.name = 'Arial'
        r_bt.font.size = Pt(11)
        r_bt.font.bold = True
        r_bt.font.color.rgb = RGBColor(0, 0, 0)

    r_txt = p.add_run(text)
    r_txt.font.name = 'Arial'
    r_txt.font.size = Pt(11)
    r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_1(doc, text, space_before=12, space_after=5):
    return add_p(doc, text, bold=True, font_size=11, space_before=space_before, space_after=space_after)

def add_heading_2(doc, text, space_before=9, space_after=3):
    return add_p(doc, text, bold=True, font_size=11, space_before=space_before, space_after=space_after)

def add_wokwi_link(doc, url):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r1 = p.add_run("Link del Proyecto en Wokwi: ")
    r1.font.name = 'Arial'
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p.add_run(url)
    r2.font.name = 'Arial'
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.underline = True
    r2.font.color.rgb = RGBColor(0, 0, 255)
    return p

def add_code_box(doc, title, code_content):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(7)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run(title)
    r_title.font.name = 'Arial'
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.25)
    set_cell_background(cell, "D9D9D9")
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="B0B0B0", sz="4")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    p_code = cell.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.0

    r_code = p_code.add_run(code_content.strip())
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(9)
    r_code.font.color.rgb = RGBColor(0, 0, 0)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(3)

def add_capture_placeholder(doc, capture_num, title, instructions_list):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.25)
    set_cell_background(cell, "F4F6F9")
    set_cell_borders(cell, top="dashed", bottom="dashed", left="dashed", right="dashed", color="2E5B82", sz="12")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)

    p_h = cell.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(2)
    p_h.paragraph_format.space_after = Pt(3)
    r_icon = p_h.add_run(f"ESPACIO PARA CAPTURA DE PANTALLA Nº {capture_num}\n")
    r_icon.font.name = 'Arial'
    r_icon.font.bold = True
    r_icon.font.size = Pt(10.5)
    r_icon.font.color.rgb = RGBColor(46, 91, 130)

    r_title = p_h.add_run(title.upper())
    r_title.font.name = 'Arial'
    r_title.font.bold = True
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    p_div = cell.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(3)
    r_div = p_div.add_run("─" * 58)
    r_div.font.name = 'Arial'
    r_div.font.size = Pt(8)
    r_div.font.color.rgb = RGBColor(180, 190, 200)

    p_inst = cell.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(2)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst_h = p_inst.add_run("¿Qué debe mostrar esta captura?:")
    r_inst_h.font.name = 'Arial'
    r_inst_h.font.bold = True
    r_inst_h.font.size = Pt(9)
    r_inst_h.font.color.rgb = RGBColor(46, 91, 130)

    for item in instructions_list:
        p_b = cell.add_paragraph()
        p_b.paragraph_format.left_indent = Inches(0.2)
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(2)
        p_b.paragraph_format.line_spacing = 1.05
        rb_sym = p_b.add_run("✓  ")
        rb_sym.font.name = 'Arial'
        rb_sym.font.bold = True
        rb_sym.font.size = Pt(8.5)
        rb_sym.font.color.rgb = RGBColor(0, 128, 0)

        rb_txt = p_b.add_run(item)
        rb_txt.font.name = 'Arial'
        rb_txt.font.size = Pt(8.5)
        rb_txt.font.color.rgb = RGBColor(40, 40, 40)

    p_paste = cell.add_paragraph()
    p_paste.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_paste.paragraph_format.space_before = Pt(12)
    p_paste.paragraph_format.space_after = Pt(12)
    r_paste = p_paste.add_run("[ HAGA CLIC AQUÍ Y PEGUE (Ctrl+V) SU CAPTURA DE PANTALLA ]")
    r_paste.font.name = 'Arial'
    r_paste.font.italic = True
    r_paste.font.bold = True
    r_paste.font.size = Pt(9)
    r_paste.font.color.rgb = RGBColor(120, 130, 140)

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(0)
    p_post.paragraph_format.space_after = Pt(5)

def add_guide_image(doc, img_path, caption, width_in=5.4):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(5)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Inches(width_in))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(80, 80, 80)

def add_clean_table(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Table Header (Gray D9D9D9 with black text)
    for c_idx, h_text in enumerate(headers):
        cell = tbl.rows[0].cells[c_idx]
        if col_widths:
            cell.width = Inches(col_widths[c_idx])
        set_cell_background(cell, "D9D9D9")
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="B0B0B0", sz="6")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Arial'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    for r_idx, row_vals in enumerate(data):
        row_bg = "FFFFFF" if r_idx % 2 == 0 else "F4F6F9"
        for c_idx, val in enumerate(row_vals):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            if col_widths:
                cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, row_bg)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="CCCCCC", sz="4")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

# =========================================================================
# CODE STRINGS
# =========================================================================

C1_SKETCH = """/*
 *      -----HOLA MUNDO-----
*/
void setup() {
  Serial.begin(115200);  // Se inicializa la conexion serie a 115200 baudios.
  Serial.println("Esta linea se ejecuta en el void setup.");
  Serial.println("esta es una segunda linea del void setup.");
}

void loop() {
  Serial.println(" Esta linea pertenece al void loop  ");
  Serial.println(" En otra linea --- Hola Mundo ---");
  delay(2000);
}
"""

C2_SKETCH = """/*
 *      -----LEDS CON REPORTE SERIAL-----
*/
#define verde 18      // Se definen los pines a los que estan conectados los LEDs.
#define rojo 21
#define amarillo 22

void setup() {
  Serial.begin(115200);     // Se inicializa la conexion serie a 115200 baudios.
  pinMode(verde, OUTPUT);    // Se configuran los pines como salida.
  pinMode(rojo, OUTPUT);
  pinMode(amarillo, OUTPUT);
}

void loop() {
  digitalWrite(verde, HIGH);     // high = 1    low = 0 
  Serial.println("Led Verde ON ");
  delay(1000);                  // Espera de mil milisegundos entre acciones.

  digitalWrite(rojo, HIGH);
  Serial.println("Led rojo ON ");
  delay(1000);

  digitalWrite(amarillo, HIGH);
  Serial.println("Led amarillo ON ");
  delay(1000);

  digitalWrite(verde, LOW);
  Serial.println("Led VERDE OFF ");
  delay(1000);

  digitalWrite(rojo, LOW);
  Serial.println("Led ROJO OFF ");
  delay(1000);

  digitalWrite(amarillo, LOW);
  Serial.println("Led AMARILLO OFF ");
  delay(1000);
}
"""

C3_SKETCH = """/*
 *      -----TEST SENSORES DHT22 Y POTENCIOMETRO-----
*/
#include "DHT.h"             // incluimos el modulo de temperatura
#define pin1 13

int pin2 = 34;               // GPIO 34 (ADC1_CH6)
DHT dht(pin1, DHT22);        // El sensor blanco (DHT11 es el azul)

void setup() {
  Serial.begin(115200);
  Serial.println("Test de sensores:");
  dht.begin();
}

void loop() {
  delay(500);
  leerdht();
  delay(500);
  leerpot();
}

void leerdht() {
  float h = dht.readHumidity();            // Leemos la Humedad
  float tc = dht.readTemperature();        // Leemos la temperatura en Celsius
  float tf = dht.readTemperature(true);    // Leemos la temperatura en Fahrenheit
  float st = dht.computeHeatIndex(tc, h);  // Sensacion Termica
  Serial.println("Temperatura: " + String(tc) + " °C ");
  Serial.println("Humedad: " + String(h) + " %");
  Serial.println("Temperatura: " + String(tf) + " °F ");
  Serial.println("Sensación Térmica: " + String(st) + " °C");
  Serial.println("--------------------------------------------");
  delay(2000);
}

void leerpot() {
  int potValor = analogRead(pin2);
  float vol = potValor * 3.3 / 4095.0;
  Serial.println("Lectura ADC binario: " + String(potValor));
  Serial.println("Voltaje medido     : " + String(vol, 2) + " V");
  Serial.println("--------------------------------------------");
  delay(500);
}
"""

C4_SKETCH = """// Agregamos librerias
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// CONFIGURACION WIFI ==================
#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

// ADAFRUIT IO ==================
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883

#define AIO_USERNAME    "gianfranco_arocutipa"
#define AIO_KEY         "xxxxxxxxxxxxxxxxxxxxxxxxxxx"

// PINES ==================
#define DHTPIN 13
#define DHTTYPE DHT22
int pin2 = 34;          // ADC1_CH6

WiFiClient client;

// Crear cliente MQTT
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT,
                          AIO_USERNAME, AIO_KEY);

// Feeds de Adafruit
Adafruit_MQTT_Publish temperatura =
  Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/DHT22");

Adafruit_MQTT_Publish voltaje =
  Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Potenciometro");

DHT dht(DHTPIN, DHTTYPE);

void conectarMQTT();

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Conectando WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi conectado");
}

void loop() {
  conectarMQTT();
  leerdht();
  leerpot();
  Serial.println("Datos enviados a Adafruit IO");
  Serial.println("--------------------------------");
  delay(7000);
}

// Leer temperatura ----------------------------------------------------
void leerdht() {
  float tc = dht.readTemperature();
  if (!isnan(tc)) {
    Serial.println("Temperatura : " + String(tc) + " °C");
    temperatura.publish(tc);
  }
}

// Leer potenciometro -------------------------------------------
void leerpot() {
  int lectura = analogRead(pin2);
  // Conversion a voltaje (ESP32 ADC de 12 bits: 0 a 4095)
  float vol = lectura * 3.3 / 4095.0;
  Serial.println("ADC      : " + String(lectura));
  Serial.println("Voltaje  : " + String(vol) + " V");
  voltaje.publish(vol);
}

// conectar al MQTT --------------------------------------------
void conectarMQTT() {
  int8_t ret;
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Conectando a Adafruit IO... ");
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Reintentando en 5 segundos...");
    mqtt.disconnect();
    delay(5000);
  }
  Serial.println("Conectado");
}
"""

C5_SKETCH = """// CUESTIONARIO INTEGRAL: PUBLICACION DE 5 FEEDS EN ADAFRUIT IO
// Publica: Temperatura, Humedad, Sensacion Termica, Potenciometro 1 y Potenciometro 2
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// Configuracion WiFi
#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

// Servidor y Credenciales Adafruit IO
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "FabrizioPerezPeralta"
#define AIO_KEY         "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx"

// Pines
#define DHTPIN 13
#define DHTTYPE DHT22
const int pinPot1 = 34; // Potenciometro 1 (ADC1 - Canal 6)
const int pinPot2 = 35; // Potenciometro 2 (ADC1 - Canal 7)

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// 5 Feeds requeridos por el cuestionario oficial (verificados en Dashboard Dash_DHT22_LAB03IOT)
Adafruit_MQTT_Publish feedTemp     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/DHT22");
Adafruit_MQTT_Publish feedHum      = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/humedad");
Adafruit_MQTT_Publish feedSensTerm = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/sensacion-termica");
Adafruit_MQTT_Publish feedPot1     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Potenciometro1");
Adafruit_MQTT_Publish feedPot2     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Potenciometro2");

DHT dht(DHTPIN, DHTTYPE);

void conectarMQTT();

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Iniciando conexion WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi conectado exitosamente");
}

void loop() {
  conectarMQTT();

  // 1. Lectura del DHT22 (Temperatura, Humedad, Sensacion Termica)
  float h = dht.readHumidity();
  float tc = dht.readTemperature();
  if (!isnan(h) && !isnan(tc)) {
    float st = dht.computeHeatIndex(tc, h, false);
    Serial.println("[DHT22] Temp: " + String(tc, 1) + " °C | Hum: " + String(h, 1) + " % | Sens.Term: " + String(st, 1) + " °C");
    feedTemp.publish(tc);
    feedHum.publish(h);
    feedSensTerm.publish(st);
  }

  // 2. Lectura Potenciometro 1 (GPIO 34 - ADC1)
  int val1 = analogRead(pinPot1);
  float vol1 = val1 * 3.3 / 4095.0;
  Serial.println("[POT 1] ADC: " + String(val1) + " | Voltaje: " + String(vol1, 2) + " V");
  feedPot1.publish(vol1);

  // 3. Lectura Potenciometro 2 (GPIO 35 - ADC1)
  int val2 = analogRead(pinPot2);
  float vol2 = val2 * 3.3 / 4095.0;
  Serial.println("[POT 2] ADC: " + String(val2) + " | Voltaje: " + String(vol2, 2) + " V");
  feedPot2.publish(vol2);

  Serial.println("-> 5 Feeds transmitidos a Adafruit IO con exito.");
  Serial.println("----------------------------------------------------------");
  delay(7000);
}

void conectarMQTT() {
  int8_t ret;
  if (mqtt.connected()) return;

  Serial.print("Conectando con Adafruit IO MQTT... ");
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Reintentando en 5 segundos...");
    mqtt.disconnect();
    delay(5000);
  }
  Serial.println("Conectado");
}
"""

def generate_report_docx(output_dir, assets_dir, images_dir):
    doc = docx.Document()
    setup_page_layout(doc, assets_dir)

    print("Building Portada (Lab 2 Style)...")
    # PORTADA
    add_p(doc, "UNIVERSIDAD PRIVADA DE TACNA", bold=True, font_size=18, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_p(doc, "FACULTAD DE INGENIERÍA", bold=True, font_size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "ESCUELA DE INGENIERÍA DE SISTEMAS", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    c_logo = os.path.join(assets_dir, 'cover_logo_5.png')
    if os.path.exists(c_logo):
        p_c_img = doc.add_paragraph()
        p_c_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c_img.paragraph_format.space_before = Pt(4)
        p_c_img.paragraph_format.space_after = Pt(14)
        p_c_img.add_run().add_picture(c_logo, width=Inches(2.45))

    add_p(doc, "Guía Práctica de Laboratorio", bold=True, font_size=20, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4)
    add_p(doc, "“PLACA Esp32”", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=16)

    add_p(doc, "Que se presenta para el curso:", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "“INTERNET DE LAS COSAS”", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=18)

    add_p(doc, "Docente:", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "Mgr. Alex Juan Yanqui Constancio", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    add_p(doc, "Estudiantes:", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "Perez Peralta, Fabrizio Salvador Elias – 2023077476", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Arocutipa Arocutipa, Gian Franco - 2023076790", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24)

    add_p(doc, "TACNA – PERÚ", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=2)
    add_p(doc, "2026", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0)

    doc.add_page_break()

    print("Building Índice General (Lab 2 Style)...")
    # ÍNDICE GENERAL
    add_p(doc, "Índice General", bold=True, font_size=11, space_before=10, space_after=10)

    toc_items = [
        ("Introducción", "3"),
        ("1.   Información sobre el evento práctico", "4"),
        ("      1.1.   Título del evento práctico", "4"),
        ("      1.2.   Objetivos", "4"),
        ("      1.3.   Tiempo de duración (horas)", "4"),
        ("      1.4.   Resultados de Aprendizaje (RA)", "4"),
        ("      1.5.   Recursos (Equipos, materiales, programas y otros)", "4"),
        ("      1.6.   Ventajas del ESP32 y Adafruit IO en IoT", "4"),
        ("2.   Procedimiento o Metodología", "5"),
        ("      2.1.   Instalando Plugin del ESP32 para Arduino", "5"),
        ("      2.2.   MONTAJE y Pinout del ESP32 DevKit v1", "6"),
        ("      2.3.   Circuito 1: Programa Hola Mundo de Ejemplo (UART 115200 baudios)", "7"),
        ("      2.4.   Circuito 2: Prueba con LEDs (Salidas Digitales GPIO)", "9"),
        ("      2.5.   Modificación del Semáforo con Puerto Serial", "10"),
        ("      2.6.   Circuito 3: Prueba con Sensor DHT22 y Potenciómetro Analógico (ADC)", "12"),
        ("      2.7.   Configuración de la Plataforma Cloud Adafruit IO (Feeds y Dashboards)", "14"),
        ("      2.8.   Circuito 4: Conexión WiFi + Adafruit IO mediante MQTT", "16"),
        ("      2.9.   Circuito 5: Resolución del Cuestionario Integrador (5 Feeds y 2 Potenciómetros)", "18"),
        ("3.   Análisis Teórico y Cálculos de Ingeniería", "20"),
        ("      3.1.   Cuantización y Resolución del ADC de 12 Bits del ESP32", "20"),
        ("      3.2.   Dimensionamiento de Resistencias para LEDs a 3.3V", "20"),
        ("      3.3.   Comparativa de Overhead y Rendimiento: Protocolo MQTT vs HTTP en IoT", "20"),
        ("      3.4.   Restricción de Canales ADC con WiFi Activo (ADC1 vs ADC2)", "21"),
        ("4.   Conclusiones", "22"),
        ("5.   Referencias Bibliográficas", "23"),
        ("6.   Anexos", "24")
    ]

    for title, page_no in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(2.5)
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        r_t1 = p_t.add_run(title)
        r_t1.font.name = 'Arial'
        r_t1.font.size = Pt(11)
        r_t1.font.color.rgb = RGBColor(0, 0, 0)
        
        r_tab = p_t.add_run('\t')
        r_tab.font.name = 'Arial'
        r_tab.font.size = Pt(11)

        r_pgn = p_t.add_run(page_no)
        r_pgn.font.name = 'Arial'
        r_pgn.font.size = Pt(11)
        r_pgn.font.bold = True
        r_pgn.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    print("Building Introducción (Lab 2 Style)...")
    # INTRODUCCIÓN
    add_p(doc, "Introducción", bold=True, font_size=11, space_before=10, space_after=8)

    add_p(doc, "ESP32 es la denominación de una familia de chips SoC de bajo costo y consumo de energía, con tecnología Wi-Fi y Bluetooth de modo dual integrada. El ESP32 emplea un microprocesador Tensilica Xtensa LX6 en sus variantes de simple y doble núcleo e incluye interruptores de antena, balun de radiofrecuencia, amplificador de potencia, amplificador receptor de bajo ruido, filtros y módulos de administración de energía. Creado por Espressif Systems y fabricado en proceso de 40 nm, representa el estándar industrial para el desarrollo ágil de sistemas embebidos e Internet de las Cosas (IoT).")

    add_p(doc, "Frente a plataformas clásicas de 8 bits como el ATmega328P de Arduino Uno o Nano, el ESP32 ofrece un salto cuántico de rendimiento: procesador de 32 bits a 240 MHz, 520 KB de memoria SRAM interna y soporte nativo para sistemas operativos en tiempo real (FreeRTOS) y pilas de comunicación completas (TCP/IP). Esto permite ejecutar algoritmos de sensado analógico y digital en paralelo con transmisiones inalámbricas de alta velocidad.")

    add_p(doc, "Para la adquisición de magnitudes físicas, el sistema integra el sensor digital DHT22 para el monitoreo de temperatura y humedad mediante comunicación digital de un solo hilo, así como dos convertidores analógico a digital (ADC) de 12 bits para digitalizar señales de transductores resistivos como potenciómetros.")

    add_p(doc, "Asimismo, para la telegestión de datos en la nube se emplea la plataforma Adafruit IO basada en el protocolo ligero MQTT (Message Queuing Telemetry Transport). A través del esquema de publicación y suscripción sobre el puerto TCP 1883, el ESP32 envía periódicamente telemetría hacia canales denominados 'Feeds', desplegando medidores angulares y gráficos temporales interactivos en paneles de control (Dashboards). Todo el ecosistema se valida virtualmente mediante el simulador Wokwi sobre la red Wi-Fi 'Wokwi-GUEST'.")

    doc.add_page_break()

    print("Building Sección 1: Información...")
    # SECCIÓN 1: INFORMACIÓN
    add_p(doc, "Guía de Laboratorio Nº9 “PLACA Esp32”", bold=True, font_size=11, space_before=8, space_after=6)
    add_heading_1(doc, "1. Información sobre el evento práctico")

    add_heading_2(doc, "1.1. Título del evento práctico")
    add_p(doc, "PLACA Esp32")

    add_heading_2(doc, "1.2. Objetivos")
    add_bullet(doc, "Configurar la placa Esp32 en Arduino IDE y la plataforma de simulación en línea Wokwi.")
    add_bullet(doc, "Accesar a los sensores vía Wokwi mediante entradas digitales y analógicas.")
    add_bullet(doc, "Implementar la comunicación serial a 115200 baudios y el control de salidas digitales GPIO.")
    add_bullet(doc, "Conectar el ESP32 a la red Wi-Fi y transmitir telemetría hacia la nube de Adafruit IO vía MQTT.")
    add_bullet(doc, "Resolver el cuestionario integrador publicando simultáneamente 5 feeds con dos potenciómetros y DHT22.")

    add_heading_2(doc, "1.3. Tiempo de duración (horas)")
    add_p(doc, "02 horas.")

    add_heading_2(doc, "1.4. Resultados de Aprendizaje (RA)")
    add_bullet(doc, "Configura controlador Esp32.", bold_prefix="RA1: ")
    add_bullet(doc, "Configura sensores y actuadores en Wokwi e integra telemetría cloud.", bold_prefix="RA2: ")

    add_heading_2(doc, "1.5. Recursos (Equipos, materiales, programas y otros)")
    add_bullet(doc, "Computador personal con navegador web y conexión a Internet.")
    add_bullet(doc, "IDE de Arduino (versión 1.8.x o superior / Arduino IDE 2.x).")
    add_bullet(doc, "Plataforma de simulación Wokwi (https://wokwi.com).")
    add_bullet(doc, "1 Placa ESP32 DevKit v1.")
    add_bullet(doc, "1 Sensor digital de temperatura y humedad DHT22.")
    add_bullet(doc, "2 Potenciómetros lineales de 10 kΩ.")
    add_bullet(doc, "3 LEDs (Verde, Rojo y Amarillo) y 3 resistencias de 220 Ω.")
    add_bullet(doc, "Cuenta activa en Adafruit IO (https://io.adafruit.com).")

    add_heading_2(doc, "1.6. Ventajas del ESP32 y Adafruit IO en IoT")
    add_bullet(doc, "El ESP32 opera a 32 bits y 240 MHz con conectividad Wi-Fi y Bluetooth nativa, superando las limitaciones de memoria de placas de 8 bits.")
    add_bullet(doc, "El protocolo MQTT minimiza el consumo de datos al utilizar encabezados fijos de solo 2 bytes, permitiendo transmisiones periódicas altamente eficientes.")
    add_bullet(doc, "Wokwi emula la CPU Xtensa del ESP32 y su radio Wi-Fi sin requerir hardware físico, reduciendo riesgos de daño por conexionado.")

    doc.add_page_break()

    print("Building Sección 2: Procedimiento...")
    # SECCIÓN 2: PROCEDIMIENTO
    add_heading_1(doc, "2. Procedimiento o Metodología")

    add_heading_2(doc, "2.1 Instalando Plugin del ESP32 para Arduino")
    add_p(doc, "Este paso es necesario para que el IDE de Arduino reconozca al ESP32 como una tarjeta de desarrollo:")
    add_num_item(doc, "1", "Ir a: Archivo > Preferencias, y en la casilla 'Gestor de URLs Adicionales de Tarjetas' agregar la URL estable oficial de Espressif: https://espressif.github.io/arduino-esp32/package_esp32_index.json")
    add_num_item(doc, "2", "Seguidamente ir a: Herramientas > Placa > Gestor de Tarjetas, buscar en la lista 'esp32' de Espressif Systems y hacer clic en Instalar.")
    add_num_item(doc, "3", "En Herramientas > Placa, seleccionar 'DOIT ESP32 DEVKIT V1' (o 'ESP32 Dev Module') y fijar la velocidad del monitor serie en 115200 baudios.")

    add_heading_2(doc, "2.2 MONTAJE y Pinout del ESP32 DevKit v1")
    add_p(doc, "La placa ESP32 DevKit v1 expone los pines del SoC. Es crucial considerar que la lógica del ESP32 es de 3.3V (no tolerante a 5V en entradas puras). Además, las entradas analógicas se agrupan en ADC1 y ADC2:")
    add_bullet(doc, "ADC1 (GPIO 32 a 39): Completamente funcional de forma continua, incluso con el Wi-Fi activado.")
    add_bullet(doc, "ADC2 (GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27): Es compartido con el circuito de radio Wi-Fi. Al iniciar la conexión inalámbrica, el ADC2 se desactiva para lecturas analógicas.")

    img_pinout = os.path.join(images_dir, 'page_8_img_2_Image87.png')
    add_guide_image(doc, img_pinout, "Figura 1: Distribución oficial de pines y canales ADC1/ADC2 del ESP32 DevKit v1", width_in=4.8)

    # -------------------------------------------------------------------------
    # CIRCUITO 1: HOLA MUNDO
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.3. Circuito 1: Programa Hola Mundo de Ejemplo (UART 115200 baudios)")
    add_p(doc, "El primer circuito valida la compilación, carga del firmware y comunicación serial asíncrona a 115200 baudios a través de la UART0 integrada del ESP32.")

    add_wokwi_link(doc, "https://wokwi.com/projects/478342840645745665")

    img_c1_sim = os.path.join(images_dir, 'c1_wokwi_holamundo.png')
    add_guide_image(doc, img_c1_sim, "Figura 2: Simulación del Circuito 1 en Wokwi mostrando la inicialización del ESP32 DevKit y la transmisión en bucle del mensaje 'Hola Mundo' por el Monitor Serial a 115200 baudios.", width_in=3.6)

    img_c1_ser = os.path.join(images_dir, 'page_9_img_2_Image94.png')
    add_guide_image(doc, img_c1_ser, "Figura 3: Salida de verificación en el Monitor Serial del ESP32 a 115200 baudios según la guía oficial.", width_in=3.8)

    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 1 - Hola Mundo ESP32)", C1_SKETCH)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "Comprueba la comunicación serie directa entre la UART0 del ESP32 y la consola virtual a 115200 baudios, verificando la inicialización del procesador y el reloj base sin requerir sensores ni actuadores externos.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Inicializa la UART0 a 115200 baudios (velocidad nativa del ESP32).", "Serial.begin(115200)")
    add_num_item(doc, "2", "Imprime los mensajes de arranque una sola vez al iniciar.", "setup()")
    add_num_item(doc, "3", "Transmite continuamente el saludo 'Hola Mundo' con pausas de 2 segundos.", "loop()")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "La consola serial recibe los mensajes limpios y sincronizados al presionar Play.")
    add_bullet(doc, "El mensaje 'Hola Mundo' se repite periódicamente cada 2000 ms sin desfases.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "La tasa de 115200 baudios es el estándar en ESP32 para evitar saturación del búfer de transmisión.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CIRCUITO 2: SEMÁFORO DE LEDS
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.4. Circuito 2: Prueba con LEDs y Modificación con Puerto Serial")
    add_p(doc, "Control secuencial de un semáforo vehicular de 3 fases mediante salidas digitales GPIO (Verde en 18, Amarillo en 22 y Rojo en 21) con resistencias de 220 Ω y reporte de estado por puerto serie.")

    add_wokwi_link(doc, "https://wokwi.com/projects/478343516314691585")

    headers_c2 = ["Componente", "Pin ESP32", "Tipo de Señal", "Función en el Circuito"]
    data_c2 = [
        ["LED Verde", "GPIO 18", "Salida Digital (HIGH/LOW)", "Indicador de paso vehicular permitido"],
        ["LED Amarillo", "GPIO 22", "Salida Digital (HIGH/LOW)", "Indicador de precaución / transición"],
        ["LED Rojo", "GPIO 21", "Salida Digital (HIGH/LOW)", "Indicador de detención obligatoria"],
        ["Resistencias (3x)", "GND", "Pasivo (220 Ω)", "Limitación de corriente a ~5.9 mA"]
    ]
    add_clean_table(doc, headers_c2, data_c2, [1.5, 1.2, 1.8, 1.75])

    img_c2_1 = os.path.join(images_dir, 'c2_wokwi_semaforo_1.png')
    add_guide_image(doc, img_c2_1, "Figura 4: Montaje circuital en Wokwi del semáforo con 3 LEDs conectado al ESP32 (GPIO 18, 21 y 22) con resistencias limitadoras de 220 Ω y monitor serial inicializado.", width_in=4.4)

    img_c2_2 = os.path.join(images_dir, 'c2_wokwi_semaforo_2.png')
    add_guide_image(doc, img_c2_2, "Figura 5: Simulación activa del semáforo con los LEDs encendidos y monitor serial sincronizado en el entorno virtual Wokwi.", width_in=4.4)

    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 2 - Semáforo de 3 LEDs con Reporte Serial)", C2_SKETCH)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "Cada LED se polariza en directa desde su respectivo GPIO a 3.3V. Las resistencias de 220 Ω limitan la corriente por diodo a ~5.9 mA, protegiendo las compuertas de salida del ESP32.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Declara los pines 18, 21 y 22 como salidas digitales de baja impedancia.", "pinMode()")
    add_num_item(doc, "2", "Enciende en secuencia cada LED por 1000 ms y reporta 'ON' por serial.", "Secuencia ON")
    add_num_item(doc, "3", "Apaga sucesivamente cada LED en el mismo orden y reporta 'OFF' por serial.", "Secuencia OFF")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "Los LEDs conmutan en ciclo continuo de 1 s por estado.")
    add_bullet(doc, "El monitor serial reporta la transición exacta de encendido y apagado de cada color.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "La corriente total con los 3 LEDs encendidos (~18 mA) es segura para el bus de alimentación del módulo.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CIRCUITO 3: DHT22 Y POTENCIÓMETRO
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.6. Circuito 3: Prueba con Sensor DHT22 y Potenciómetro Analógico (ADC)")
    add_p(doc, "Adquisición simultánea de variables climáticas con el sensor digital unifilar DHT22 (GPIO 13) y digitalización de voltaje de 0 a 3.3V mediante un potenciómetro en la entrada analógica GPIO 34 (ADC1_CH6).")

    add_wokwi_link(doc, "https://wokwi.com/projects/478344298758078465")

    headers_c3 = ["Sensor / Elemento", "Pin ESP32", "Tipo", "Rango de Medición"]
    data_c3 = [
        ["DHT22 (SDA / Datos)", "GPIO 13", "Entrada Digital Unifilar", "-40 a 80 °C (±0.5°C), 0 a 100% RH"],
        ["DHT22 (VCC / GND)", "3.3V / GND", "Alimentación", "3.3 V DC"],
        ["Potenciómetro (Señal)", "GPIO 34 (ADC1_CH6)", "Entrada Analógica", "0 a 4095 (0.00 V a 3.30 V)"],
        ["Potenciómetro (Extremos)", "3.3V / GND", "Alimentación", "Referencia fija de 3.3V"]
    ]
    add_clean_table(doc, headers_c3, data_c3, [1.8, 1.5, 1.4, 1.55])

    img_c3_1 = os.path.join(images_dir, 'c3_wokwi_dht22_pot_1.png')
    add_guide_image(doc, img_c3_1, "Figura 6: Simulación en Wokwi del Circuito 3 con potenciómetro en escala mínima (0 binario = 0.00 V) y sensor DHT22 reportando Temperatura: 24.00 °C, Humedad: 40.00 % y Sensación Térmica: 17.98 °C.", width_in=3.6)

    img_c3_2 = os.path.join(images_dir, 'c3_wokwi_dht22_pot_2.png')
    add_guide_image(doc, img_c3_2, "Figura 7: Simulación dinámica en Wokwi variando el potenciómetro a 2762 binario (2.22 V) y slider de DHT22 ajustado a 55.4 °C y 70.5 % HR.", width_in=3.4)

    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 3 - Test Sensores DHT22 y ADC)", C3_SKETCH)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "El DHT22 transmite tramas digitales calibradas de 40 bits por un solo hilo. El potenciómetro actúa como divisor resistivo ajustable, entregando un voltaje continuo al convertidor ADC1 de 12 bits para su cuantización en 4096 niveles.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Adquiere humedad (%), temperatura (°C y °F) y calcula el índice de calor (Heat Index).", "leerdht()")
    add_num_item(doc, "2", "Lee el canal ADC1_CH6 (0-4095) y calcula el voltaje real: V = ADC * 3.3 / 4095.0.", "leerpot()")
    add_num_item(doc, "3", "Imprime periódicamente los datos climáticos y analógicos en la consola serial.", "Reporte Serial")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "Al deslizar los valores del DHT22, la temperatura y sensación térmica se actualizan de inmediato.")
    add_bullet(doc, "Al girar el potenciómetro, el valor binario y el voltaje calculado varían con precisión de 0V a 3.3V.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "El pin GPIO 34 pertenece al bloque ADC1, garantizando lecturas estables e inmunes a la radio Wi-Fi.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CIRCUITO 4: WIFI + ADAFRUIT IO
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.7. Configuración de Adafruit IO y Circuito 4: Conexión WiFi + MQTT")
    add_p(doc, "Enlace telemático IoT conectando el ESP32 a la red Wi-Fi virtual 'Wokwi-GUEST' y transmitiendo periódicamente las lecturas hacia el broker MQTT 'io.adafruit.com' (puerto 1883).")

    add_wokwi_link(doc, "https://wokwi.com/projects/478344298758078465")

    img_c4_1 = os.path.join(images_dir, 'c4_wokwi_adafruit_1.png')
    add_guide_image(doc, img_c4_1, "Figura 8: Dashboard 'Dash ESP32' en Adafruit IO (cuenta GianArocutipa) enlazado con la simulación Wokwi en tiempo real, registrando Temperatura: 51.10 °C y Voltaje del potenciómetro: 2.20 V (ADC: 2732).", width_in=5.2)

    img_c4_2 = os.path.join(images_dir, 'c4_wokwi_adafruit_2.png')
    add_guide_image(doc, img_c4_2, "Figura 9: Telemetría continua MQTT en Adafruit IO ante cambios en la simulación: lectura de temperatura bajo cero (-31.70 °C con alerta visual en medidor Gauge) y potenciómetro en 2.29 V (ADC: 2838).", width_in=5.2)

    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 4 - ESP32 WiFi + Adafruit MQTT)", C4_SKETCH)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "El ESP32 se asocia a la red Wi-Fi virtual e inicia un cliente MQTT autenticado con AIO_USERNAME y AIO_KEY. Cada 7 segundos lee el sensor DHT22 y el potenciómetro, publicando los datos hacia los tópicos en la nube.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Conecta el módulo a la red local virtual mediante WiFi.begin(WLAN_SSID, WLAN_PASS).", "WiFi.begin()")
    add_num_item(doc, "2", "Autentica la sesión MQTT y establece el canal de comunicación en el puerto 1883.", "Cliente MQTT")
    add_num_item(doc, "3", "Publica temperatura (°C) y voltaje (V) en sus respectivos feeds cada 7000 ms.", "publish()")
    add_num_item(doc, "4", "Monitorea la conexión y reintenta la suscripción en caso de desconexión.", "conectarMQTT()")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "El monitor serial confirma la asignación de IP y la conexión exitosa al broker cloud.")
    add_bullet(doc, "Los bloques del Dashboard de Adafruit IO grafican las lecturas en tiempo real cada 7 segundos.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "El intervalo de 7 s respeta el límite de peticiones por minuto de la cuenta gratuita de Adafruit IO.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CIRCUITO 5: CUESTIONARIO INTEGRAL (5 FEEDS)
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.9. Circuito 5: Resolución del Cuestionario Integrador (5 Feeds y 2 Potenciómetros)")
    add_p(doc, "Resolución del cuestionario oficial (página 20): ampliación del sistema para publicar en simultáneo 5 variables (Temperatura, Humedad, Sensación Térmica, Potenciómetro 1 y Potenciómetro 2) en Adafruit IO.")

    add_wokwi_link(doc, "https://wokwi.com/projects/esp32-adafruit-5feeds-integral")

    headers_c5 = ["Feed en Adafruit IO", "Variable Física", "Fuente de Hardware", "Unidad de Medida"]
    data_c5 = [
        ["DHT22 (o temperatura)", "Temperatura Ambiental", "DHT22 (GPIO 13)", "°C"],
        ["humedad", "Humedad Relativa", "DHT22 (GPIO 13)", "% HR"],
        ["sensacion-termica", "Índice de Calor (Heat Index)", "Cálculo matemático en ESP32", "°C"],
        ["Potenciometro1", "Tensión Analógica 1", "Potenciómetro 1 (GPIO 34 - ADC1)", "Voltios (0 a 3.3 V)"],
        ["Potenciometro2", "Tensión Analógica 2", "Potenciómetro 2 (GPIO 35 - ADC1)", "Voltios (0 a 3.3 V)"]
    ]
    add_clean_table(doc, headers_c5, data_c5, [1.6, 1.6, 1.85, 1.2])

    add_heading_2(doc, "Simulación en Wokwi y Telemetría Multivariable en Adafruit IO (5 Feeds)")
    add_p(doc, "En el entorno de simulación Wokwi se montó el circuito completo con el sensor DHT22 y dos potenciómetros conectados a canales seguros del convertidor ADC1 (GPIO 34 y GPIO 35). Las siguientes capturas demuestran la recepción simultánea de los 5 feeds en el Dashboard 'Dash2 ESP32' (cuenta GianArocutipa) ante diferentes estados de simulación:")

    img_c5_1 = os.path.join(images_dir, 'c5_wokwi_cuestionario_1.png')
    add_guide_image(doc, img_c5_1, "Figura 10: Dashboard 'Dash2 ESP32' en Adafruit IO recibiendo en tiempo real los 5 feeds simultáneos desde Wokwi (Temperatura: 24 °C, Sensación Térmica: 23.5 °C, Humedad: 40 %, Potenciómetro 1: 1.89 V y Potenciómetro 2: 0.40 V).", width_in=5.4)

    img_c5_2 = os.path.join(images_dir, 'c5_wokwi_cuestionario_2.png')
    add_guide_image(doc, img_c5_2, "Figura 11: Actualización dinámica de los 5 feeds en Adafruit IO tras modificar los sensores en la simulación (Temperatura: 21.4 °C, Sensación Térmica: 20.98 °C, Humedad: 53 %, Potenciómetro 1: 1.81 V y Potenciómetro 2: 1.98 V).", width_in=5.4)

    doc.add_page_break()

    add_heading_2(doc, "Montaje y Validación en Hardware Físico Real (Laboratorio)")
    add_p(doc, "Complementando la simulación, el circuito integrador fue implementado en hardware físico real sobre protoboard en el laboratorio de la Escuela Profesional de Ingeniería de Sistemas. Se utilizó la placa de desarrollo ESP32 DevKit v1 de 30 pines, alimentada vía interfaz microUSB, interconectada con un sensor de temperatura y humedad DHT22 y dos potenciómetros rotativos analógicos cableados a los pines seguros ADC1 (GPIO 34 y GPIO 35):")

    img_real_hardware = os.path.join(images_dir, 'real_cuestionario_image2.png')
    add_guide_image(doc, img_real_hardware, "Figura 12: Montaje físico experimental en protoboard del Cuestionario Integrador utilizando tarjeta ESP32 DevKit v1, sensor digital DHT22 y dos potenciómetros analógicos conectados a canales ADC1 (GPIO 34 y GPIO 35).", width_in=4.8)

    add_heading_2(doc, "Telemetría en Vivo en Adafruit IO Cloud desde Hardware Real")
    add_p(doc, "El microcontrolador físico ESP32 ejecutó el firmware de enlace inalámbrico asociándose a la red local y transmitiendo vía MQTT hacia la nube de Adafruit IO. En el monitor del laboratorio se validó la recepción continua de telemetría en el Dashboard 'Dash_DHT22_LAB03IOT' (cuenta de usuario 'FabrizioPerezPeralta') con el sensor DHT22 registrando 27.9 °C y ambos potenciómetros ajustados a su escala máxima (3.30 V):")

    img_real_dashboard = os.path.join(images_dir, 'real_cuestionario_image1.png')
    add_guide_image(doc, img_real_dashboard, "Figura 13: Recepción y visualización telemática en tiempo real en el Dashboard 'Dash_DHT22_LAB03IOT' de Adafruit IO (cuenta: FabrizioPerezPeralta) desde el montaje físico, mostrando la temperatura medida por el DHT22 (27.9 °C) y los dos medidores tipo Gauge de los potenciómetros (3.3 V).", width_in=4.8)

    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 5 - Cuestionario Integrador con 5 Feeds en Adafruit IO)", C5_SKETCH)

    add_heading_2(doc, "Explicación del circuito y Justificación Técnica de ADC1")
    add_p(doc, "Se incorpora un segundo potenciómetro en GPIO 35 (canal ADC1_CH7). Se utilizan exclusivamente pines del ADC1 (GPIO 34 y 35) porque el bloque ADC2 es compartido internamente con el hardware Wi-Fi y queda bloqueado al encender la radio.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Adquiere temperatura, humedad y computa la sensación térmica desde el DHT22.", "DHT22")
    add_num_item(doc, "2", "Digitaliza en paralelo los canales analógicos GPIO 34 y 35, convirtiendo a 0-3.3V.", "ADC1 Dual")
    add_num_item(doc, "3", "Publica los 5 valores hacia sus tópicos individuales en Adafruit IO cada 7 segundos.", "Publicación")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "El microcontrolador transmite los 5 feeds en secuencia regular sin saturar el enlace.")
    add_bullet(doc, "El Dashboard de Adafruit IO refleja en paralelo los 5 bloques con lecturas dinámicas en vivo.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "La asignación estricta a ADC1 elimina cualquier interferencia entre las lecturas analógicas y la transmisión Wi-Fi.")

    doc.add_page_break()

    print("Building Sección 3: Cálculos (Lab 2 Style)...")
    # =========================================================================
    # SECCIÓN 3: CÁLCULOS
    # =========================================================================
    add_heading_1(doc, "3. Análisis Teórico y Cálculos de Ingeniería")
    add_p(doc, "A continuación se presentan los cálculos teóricos de ingeniería que fundamentan el dimensionamiento de los circuitos y la selección de protocolos en la experiencia.")

    add_heading_2(doc, "3.1. Cuantización y Resolución del ADC de 12 Bits del ESP32")
    add_p(doc, "El convertidor analógico a digital del ESP32 opera con una resolución nativa de 12 bits, dividiendo el rango dinámico de voltaje de referencia (0 a 3.3 V) en 4096 intervalos cuantizados (0 a 4095):")
    add_p(doc, "V_LSB = V_ref / (2^N - 1) = 3.30 V / 4095 ≈ 0.80586 mV / LSB", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Datos del conversor:")
    add_bullet(doc, "V_ref = 3.30 V (Tensión nominal de alimentación del regulador del ESP32).", bold_prefix="• ")
    add_bullet(doc, "N = 12 bits -> 2^12 = 4096 niveles discretos.", bold_prefix="• ")
    add_bullet(doc, "Resolución = Cada unidad leída en analogRead() representa aproximadamente 0.806 mV.", bold_prefix="• ")
    add_p(doc, "Ejemplo de lectura intermedia:")
    add_p(doc, "Para una lectura de ADC = 2048: V_medido = 2048 * (3.30 V / 4095) = 1.650 V (50% de la escala).", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_heading_2(doc, "3.2. Dimensionamiento de Resistencias para LEDs a 3.3V")
    add_p(doc, "Para proteger las salidas GPIO del microcontrolador y los diodos LED se calcula la resistencia en serie mediante la Ley de Ohm:")
    add_p(doc, "R = (V_GPIO - V_F) / I_F", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Datos para el circuito a 3.3V:")
    add_bullet(doc, "V_GPIO = 3.30 V (Tensión de salida en estado HIGH del ESP32).", bold_prefix="• ")
    add_bullet(doc, "V_F (LED Verde / Amarillo) ≈ 2.00 V; V_F (LED Rojo) ≈ 1.80 V.", bold_prefix="• ")
    add_bullet(doc, "I_F recomendada = 6 mA = 0.006 A (iluminación óptima con bajo consumo de potencia).", bold_prefix="• ")
    add_p(doc, "Cálculo para LED Verde:")
    add_p(doc, "R = (3.30 V - 2.00 V) / 0.006 A = 1.30 V / 0.006 A = 216.67 Ω", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Se selecciona el valor comercial estándar más cercano: R = 220 Ω.")
    add_p(doc, "Corriente real resultante: I_real = (3.30 V - 2.00 V) / 220 Ω = 5.91 mA (seguro para el GPIO, cuyo límite es 12 mA).")

    add_heading_2(doc, "3.3. Comparativa de Overhead y Rendimiento: Protocolo MQTT vs HTTP en IoT")
    add_p(doc, "La selección de MQTT frente a HTTP para telemetría continua se sustenta en la reducción drástica de la sobrecarga de datos en red:")

    headers_mqtt = ["Criterio de Evaluación", "Protocolo MQTT (Usado en Lab)", "Protocolo HTTP (REST Clásico)"]
    data_mqtt = [
        ["Tamaño Mínimo de Cabecera", "2 Bytes (Ultra ligero)", "500 - 800 Bytes (Cabeceras extensas)"],
        ["Gestión de Conexión TCP", "Mantiene socket abierto (Keep-Alive)", "Abre y cierra conexión por cada petición"],
        ["Consumo de Ancho de Banda", "Muy Bajo (~90% menor consumo de datos)", "Alto (Sobrecarga de texto ASCII)"],
        ["Consumo Energético en Batería", "Mínimo (Menor tiempo de radio activo)", "Elevado (Mayor tiempo en transmisión)"],
        ["Modelo de Comunicación", "Publish / Subscribe asíncrono", "Request / Response síncrono"]
    ]
    add_clean_table(doc, headers_mqtt, data_mqtt, [1.8, 2.2, 2.25])

    add_heading_2(doc, "3.4. Restricción de Canales ADC con WiFi Activo (ADC1 vs ADC2)")
    add_bullet(doc, "Causa del Conflicto: El bloque ADC2 utiliza internamente los mismos registros de conmutación de antena y amplificación del módulo de radio Wi-Fi/Bluetooth. Al ejecutar WiFi.begin(), el driver de red bloquea el ADC2.")
    add_bullet(doc, "Impacto: Cualquier lectura de analogRead() en pines de ADC2 (GPIO 0, 2, 4, 12-15, 25-27) retorna valores nulos o corruptos durante la transmisión inalámbrica.")
    add_bullet(doc, "Solución de Ingeniería: En el Circuito 4 y Circuito 5 se asignaron los potenciómetros exclusivamente a los canales ADC1 (GPIO 34 y GPIO 35), asegurando telemetría continua sin interrupciones.")

    doc.add_page_break()

    print("Building Sección 4: Conclusiones (Lab 2 Style)...")
    # =========================================================================
    # SECCIÓN 4: CONCLUSIONES
    # =========================================================================
    add_heading_1(doc, "4. Conclusiones")

    conclusiones = [
        "Se logró la configuración exitosa del microcontrolador ESP32 DevKit v1 tanto en Arduino IDE como en la plataforma de simulación en línea Wokwi, validando la compilación y subida de firmware con salida serial asíncrona a 115200 baudios.",
        "El control de salidas digitales GPIO (Circuito 2) demostró la polarización adecuada de diodos LED a niveles lógicos de 3.3V, verificando que resistencias limitadoras de 220 Ω aseguran una corriente de 5.9 mA, protegiendo las compuertas internas del microcontrolador.",
        "La adquisición con el sensor digital DHT22 y el potenciómetro (Circuito 3) demostró la capacidad del ESP32 para procesar simultáneamente protocolos unifilares digitales y lecturas analógicas de 12 bits con una resolución de 0.806 mV/LSB.",
        "La conexión a la red Wi-Fi virtual Wokwi-GUEST permitió establecer un canal TCP robusto hacia el broker io.adafruit.com sobre el puerto 1883 sin requerir pasarelas de hardware físicas.",
        "Se comprobó la superioridad del protocolo MQTT sobre HTTP para aplicaciones IoT en tiempo real: su cabecera fija de 2 bytes redujo en más de un 90% la sobrecarga de red frente a transacciones HTTP convencionales.",
        "Se resolvió íntegramente el cuestionario oficial integrando dos potenciómetros y el sensor DHT22, transmitiendo en tiempo real hacia 5 feeds distintos de Adafruit IO de manera periódica.",
        "Se confirmó la restricción de hardware del ESP32 que inhabilita los canales ADC2 durante operaciones Wi-Fi activas, validando el uso exclusivo de los canales ADC1 (GPIO 34 y 35) para garantizar lecturas analógicas estables.",
        "La plataforma Adafruit IO demostró su eficacia para el despliegue de paneles de telemetría IoT mediante bloques tipo Gauge y gráficos temporales interactivos alimentados desde la simulación."
    ]

    for i, c in enumerate(conclusiones, 1):
        add_num_item(doc, str(i), c, space_after=4)

    doc.add_page_break()

    print("Building Sección 5: Referencias (Lab 2 Style)...")
    # =========================================================================
    # SECCIÓN 5: REFERENCIAS BIBLIOGRÁFICAS
    # =========================================================================
    add_heading_1(doc, "5. Referencias Bibliográficas")

    referencias = [
        "Ortiz Arciniega, J. L., Valencia Barahona, F. X., & colaboradores. (2025). ESP32: Manual básico para estudiantes. Alumni Editora Ecuador, Atuntaqui.",
        "Burgoa Román, F. J. (2026). Microcontrolador ESP32-S3: curso práctico (1.ª ed.). RA-MA Editorial. Recuperado de https://elibro.net/es/lc/bibliotecaupt/titulos/294849",
        "Espressif Systems. (2024). ESP32 Series Datasheet (v4.3). Espressif Systems Co., Ltd. https://www.espressif.com",
        "Adafruit Industries. (2025). Adafruit IO Basics: MQTT API Reference Guide. Adafruit Learning System. https://learn.adafruit.com/welcome-to-adafruit-io",
        "Banzi, M. y Shiloh, M. (2022). Getting Started with Arduino (4th ed.). Maker Media, Inc."
    ]

    for ref in referencias:
        add_bullet(doc, ref, space_after=5)

    doc.add_page_break()

    print("Building Sección 6: Anexos (Lab 2 Style)...")
    # =========================================================================
    # SECCIÓN 6: ANEXOS
    # =========================================================================
    add_heading_1(doc, "6. Anexos")
    add_heading_2(doc, "6.1. Guía Rápida de Conexión Wokwi con Adafruit IO")
    add_num_item(doc, "1", "Crear una cuenta gratuita en https://io.adafruit.com y abrir la pestaña 'Dashboards' para generar un nuevo panel de control.")
    add_num_item(doc, "2", "Obtener las credenciales personales (Username y AIO Key) desde el botón 'My Key' (icono de llave amarilla en la barra superior).")
    add_num_item(doc, "3", "En el simulador Wokwi, abrir el archivo 'libraries.txt' y asegurarse de tener instaladas las librerías: 'Adafruit MQTT Library' y 'DHT sensor library'.")
    add_num_item(doc, "4", "Configurar en sketch.ino el SSID como 'Wokwi-GUEST' y la contraseña vacía (\"\"). El gateway virtual de Wokwi conectará automáticamente el ESP32 a Internet.")
    add_num_item(doc, "5", "Iniciar la simulación presionando 'Play': los datos se transmitirán en vivo hacia los feeds y se graficarán automáticamente en el Dashboard.")

    # Target filenames to save
    filenames_to_save = [
        os.path.join(output_dir, "lab 3u2.docx"),
        os.path.join(output_dir, "lab 3.docx"),
        os.path.join(output_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx"),
        os.path.join(output_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit_Actualizado.docx"),
        os.path.join(output_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 3u2 Esp32 Wokwi - Adafruit.docx")
    ]
    for fn in filenames_to_save:
        try:
            doc.save(fn)
            print(f"Document saved successfully: {fn}")
        except Exception as e:
            print(f"Error saving {fn}: {e}")

def export_docx_to_pdf(docx_path, pdf_path):
    """Exports DOCX to PDF using native Word application."""
    import win32com.client
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
        doc.Close()
        print(f"PDF exported successfully: {pdf_path}")
        return True
    except Exception as e:
        print(f"Warning: Could not export PDF via Word for {docx_path}: {e}")
        return False
    finally:
        if word:
            try:
                word.Quit()
            except Exception:
                pass

def main():
    lab3_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(lab3_dir, "extracted_assets")
    images_dir = os.path.join(lab3_dir, "extracted_images")

    print("[1/4] Generando informes Word (.docx) con formato y estilos oficiales...")
    generate_report_docx(lab3_dir, assets_dir, images_dir)

    # Export primary Word document to PDF
    primary_docx = os.path.join(lab3_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx")
    primary_pdf = os.path.join(lab3_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.pdf")
    
    print("[2/4] Exportando a formato PDF con fidelidad nativa de Microsoft Word...")
    if export_docx_to_pdf(primary_docx, primary_pdf):
        # Also create copies of the PDF with standard alternate names
        shutil.copy2(primary_pdf, os.path.join(lab3_dir, "Perez Fabrizio_Arocutipa Gian Franco_Lab 3u2 Esp32 Wokwi - Adafruit.pdf"))
        shutil.copy2(primary_pdf, os.path.join(lab3_dir, "lab 3u2.pdf"))
        shutil.copy2(primary_pdf, os.path.join(lab3_dir, "lab 3.pdf"))

    # Copy updated word docs and pdfs to target 'lab 3u2' folder
    print("[3/4] Sincronizando documentos e imágenes en la suite de entrega 'lab 3u2'...")
    target_lab3u2 = os.path.join(lab3_dir, "lab 3u2")
    os.makedirs(target_lab3u2, exist_ok=True)
    
    files_to_sync = [
        "lab 3u2.docx",
        "lab 3.docx",
        "lab 3u2.pdf",
        "lab 3.pdf",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.pdf",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit_Actualizado.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 3u2 Esp32 Wokwi - Adafruit.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 3u2 Esp32 Wokwi - Adafruit.pdf"
    ]
    for fname in files_to_sync:
        src = os.path.join(lab3_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target_lab3u2, fname))

    # Synchronize images into respective circuit folders
    circuit_imgs = {
        "01_Circuito1_HolaMundo_ESP32": ["c1_wokwi_holamundo.png"],
        "02_Circuito2_Semaforo_Leds_ESP32": ["c2_wokwi_semaforo_1.png", "c2_wokwi_semaforo_2.png"],
        "03_Circuito3_Sensor_DHT22_Potenciometro": ["c3_wokwi_dht22_pot_1.png", "c3_wokwi_dht22_pot_2.png"],
        "04_Circuito4_ESP32_WiFi_Adafruit_IO_MQTT": ["c4_wokwi_adafruit_1.png", "c4_wokwi_adafruit_2.png"],
        "05_Circuito5_Cuestionario_Integrador_Adafruit_5Feeds": [
            "c5_wokwi_cuestionario_1.png", "c5_wokwi_cuestionario_2.png",
            "real_cuestionario_image2.png", "real_cuestionario_image1.png"
        ]
    }
    for cfolder, img_list in circuit_imgs.items():
        dst_folder = os.path.join(target_lab3u2, cfolder)
        os.makedirs(dst_folder, exist_ok=True)
        for img_name in img_list:
            img_src = os.path.join(images_dir, img_name)
            if os.path.exists(img_src):
                shutil.copy2(img_src, os.path.join(dst_folder, img_name))

    # Re-generate zip archives
    print("[4/4] Empaquetando archivo ZIP final...")
    zip_path = os.path.join(lab3_dir, "lab 3u2.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_lab3u2):
            for file in files:
                if file.endswith(".zip"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, lab3_dir)
                zipf.write(full_path, rel_path)

    shutil.copy2(zip_path, os.path.join(lab3_dir, "lab 3.zip"))

    print("\n" + "="*70)
    print("¡INFORME FINAL Y SUITE DE LABORATORIO 3 GENERADOS CON ÉXITO!")
    print(f"Ubicación de los archivos: {lab3_dir}")
    print("="*70)

if __name__ == "__main__":
    main()

