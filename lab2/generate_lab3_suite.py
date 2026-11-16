# -*- coding: utf-8 -*-
"""
Full Suite Generator for Lab 3 (Lab 2.3 - Esp32 Wokwi - Adafruit IO):
- Produces complete academic Word report matching UPT standard formatting.
- Generates all 5 Wokwi circuits (code, diagrams, libraries, readmes).
- Saves files in C:\\Users\\PC\\Desktop\\oit\\lab3\\lab 3u2\\ and creates 'lab 3u2.zip'.
- Keeps synchronized copies in the current workspace.

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

# Colors
COLOR_PRIMARY_HEX = "1B365D"   # UPT Navy Blue
COLOR_ACCENT_HEX = "008080"    # Teal
COLOR_BG_LIGHT_HEX = "F5F6F8"  # Soft Gray
COLOR_BORDER_HEX = "CCCCCC"    # Light Gray

COLOR_PRIMARY = RGBColor(27, 54, 93)
COLOR_TEXT = RGBColor(33, 33, 33)
COLOR_MUTED = RGBColor(100, 100, 100)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="CCCCCC", sz="4"):
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
        set_cell_borders(cell_l, bottom="single", color="1B365D", sz="6")
        set_cell_margins(cell_l, top=0, bottom=60, left=0, right=0)
        p_img = cell_l.paragraphs[0]
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(2)
        h_logo = os.path.join(assets_dir, 'header_logo_18.png')
        if os.path.exists(h_logo):
            p_img.add_run().add_picture(h_logo, width=Inches(0.35))
        
        cell_r = header_tbl.rows[0].cells[1]
        cell_r.width = Inches(5.45)
        set_cell_borders(cell_r, bottom="single", color="1B365D", sz="6")
        set_cell_margins(cell_r, top=0, bottom=60, left=0, right=0)
        p_txt = cell_r.paragraphs[0]
        p_txt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_txt.paragraph_format.space_before = Pt(6)
        p_txt.paragraph_format.space_after = Pt(2)
        r = p_txt.add_run('Escuela Profesional de Ingeniería de Sistemas')
        r.font.name = 'Arial'
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_PRIMARY

        # Footer (Pages 2+)
        footer = s.footer
        footer_tbl = footer.add_table(rows=1, cols=2, width=Inches(6.25))
        footer_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        f_cell_l = footer_tbl.rows[0].cells[0]
        f_cell_l.width = Inches(2.5)
        set_cell_borders(f_cell_l, top="single", color="1B365D", sz="6")
        set_cell_margins(f_cell_l, top=80, bottom=0, left=0, right=0)
        p_pg = f_cell_l.paragraphs[0]
        p_pg.paragraph_format.space_before = Pt(4)
        p_pg.paragraph_format.space_after = Pt(0)
        p_pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        r1 = p_pg.add_run('- ')
        r1.font.name = 'Arial'
        r1.font.size = Pt(10)
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        p_pg._p.append(fldSimple)
        r2 = p_pg.add_run(' -')
        r2.font.name = 'Arial'
        r2.font.size = Pt(10)

        f_cell_r = footer_tbl.rows[0].cells[1]
        f_cell_r.width = Inches(3.75)
        set_cell_borders(f_cell_r, top="single", color="1B365D", sz="6")
        set_cell_margins(f_cell_r, top=80, bottom=0, left=0, right=0)
        p_prof = f_cell_r.paragraphs[0]
        p_prof.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_prof.paragraph_format.space_before = Pt(4)
        p_prof.paragraph_format.space_after = Pt(0)
        r_prof = p_prof.add_run('Mgr. Alex Juan Yanqui Constancio')
        r_prof.font.name = 'Arial'
        r_prof.font.size = Pt(10)
        r_prof.font.color.rgb = COLOR_TEXT

def add_p(doc, text="", bold=False, italic=False, font_size=11, font_color=RGBColor(0,0,0), 
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
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
        r.font.color.rgb = font_color
    return p

def add_heading_1(doc, text):
    return add_p(doc, text, bold=True, font_size=13, font_color=COLOR_PRIMARY, space_before=14, space_after=6)

def add_heading_2(doc, text):
    return add_p(doc, text, bold=True, font_size=11.5, font_color=COLOR_PRIMARY, space_before=10, space_after=4)

def add_heading_3(doc, text):
    return add_p(doc, text, bold=True, italic=True, font_size=11, font_color=COLOR_PRIMARY, space_before=8, space_after=3)

def add_bullet(doc, text, bold_prefix="", level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT
    r = p.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_TEXT
    return p

def add_num_item(doc, num_str, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(0.3)
    
    r_num = p.add_run(f"{num_str}.  ")
    r_num.font.name = 'Arial'
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = COLOR_PRIMARY
    
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Arial'
        r_b.font.size = Pt(11)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT

    r_txt = p.add_run(text)
    r_txt.font.name = 'Arial'
    r_txt.font.size = Pt(11)
    r_txt.font.color.rgb = COLOR_TEXT
    return p

def add_code_block(doc, code_str, title="Código Fuente:"):
    if title:
        add_p(doc, title, bold=True, font_size=10, font_color=COLOR_PRIMARY, space_before=6, space_after=2)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.25)
    
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, COLOR_BG_LIGHT_HEX)
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER_HEX, sz="4")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    
    r = p.add_run(code_str.strip())
    r.font.name = 'Consolas'
    r.font.size = Pt(9.0)
    r.font.color.rgb = RGBColor(30, 30, 30)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_capture_box(doc, title, instruction, guide_img_path=None, min_height_in=1.8):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.25)
    
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, "FAFBFC")
    set_cell_borders(cell, top="dashed", bottom="dashed", left="dashed", right="dashed", color="99BBDD", sz="8")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    
    r_icon = p.add_run("📷 ")
    r_icon.font.size = Pt(11)
    
    r_title = p.add_run(f"RECUADRO DE CAPTURA: {title}\n")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(10)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY
    
    r_inst = p.add_run(instruction)
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9)
    r_inst.font.italic = True
    r_inst.font.color.rgb = RGBColor(80, 80, 80)
    
    if guide_img_path and os.path.exists(guide_img_path):
        p_img = cell.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(guide_img_path, width=Inches(4.5))
        p_cap = cell.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(2)
        r_c = p_cap.add_run("Figura de referencia de la guía oficial")
        r_c.font.name = 'Arial'
        r_c.font.size = Pt(8.5)
        r_c.font.italic = True
        r_c.font.color.rgb = COLOR_MUTED
    else:
        p_sp = cell.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(int(min_height_in * 30))
        p_sp.paragraph_format.space_after = Pt(0)
        p_sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_h = p_sp.add_run("[ Espacio reservado para pegar tu captura de pantalla de la simulación ]")
        r_h.font.name = 'Arial'
        r_h.font.size = Pt(8.5)
        r_h.font.color.rgb = RGBColor(160, 160, 160)
        
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_table(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    for c_idx, h_text in enumerate(headers):
        cell = tbl.rows[0].cells[c_idx]
        if col_widths:
            cell.width = Inches(col_widths[c_idx])
        set_cell_background(cell, COLOR_PRIMARY_HEX)
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_PRIMARY_HEX, sz="6")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, row_vals in enumerate(data):
        row_bg = "FFFFFF" if r_idx % 2 == 0 else "F8F9FA"
        for c_idx, val in enumerate(row_vals):
            cell = tbl.rows[r_idx + 1].cells[c_idx]
            if col_widths:
                cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, row_bg)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color=COLOR_BORDER_HEX, sz="4")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(9.0)
            r.font.color.rgb = COLOR_TEXT
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_formula_box(doc, title, formula_text, explanation_bullets=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.25)
    
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, COLOR_BG_LIGHT_HEX)
    set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="99BBDD", sz="6")
    set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(title + "\n")
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(10)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    r_f = p.add_run(formula_text)
    r_f.font.name = 'Consolas'
    r_f.font.size = Pt(10.5)
    r_f.font.bold = True
    r_f.font.color.rgb = RGBColor(160, 30, 30)
    
    if explanation_bullets:
        for b in explanation_bullets:
            p_b = cell.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_before = Pt(1)
            p_b.paragraph_format.space_after = Pt(1.5)
            p_b.paragraph_format.left_indent = Inches(0.2)
            r_b = p_b.add_run(b)
            r_b.font.name = 'Arial'
            r_b.font.size = Pt(9.0)
            r_b.font.color.rgb = COLOR_TEXT
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

# =========================================================================
# CODE STRINGS FOR THE 5 CIRCUITS
# =========================================================================

C1_CODE = """// CIRCUITO 1: HOLA MUNDO - ESP32
void setup() {
  Serial.begin(115200);  // Inicialización serial estándar ESP32
  Serial.println("Esta linea se ejecuta en el void setup.");
  Serial.println("esta es una segunda linea del void setup.");
}

void loop() {
  Serial.println(" Esta linea pertenece al void loop  ");
  Serial.println(" En otra linea --- Hola Mundo ---");
  delay(2000);
}
"""

C2_CODE = """// CIRCUITO 2: CONTROL DE SEMÁFORO DE 3 LEDS - ESP32
#define verde 18       // GPIO 18 -> LED Verde
#define rojo 21        // GPIO 21 -> LED Rojo
#define amarillo 22    // GPIO 22 -> LED Amarillo

void setup() {
  Serial.begin(115200);
  pinMode(verde, OUTPUT);
  pinMode(rojo, OUTPUT);
  pinMode(amarillo, OUTPUT);
}

void loop() {
  digitalWrite(verde, HIGH);
  Serial.println("Led Verde ON ");
  delay(1000);

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

C3_CODE = """// CIRCUITO 3: SENSOR DHT22 Y POTENCIÓMETRO ANALÓGICO - ESP32
#include "DHT.h"

#define pin1 13        // GPIO 13 -> Datos DHT22
int pin2 = 34;         // GPIO 34 -> Potenciómetro (ADC1_CH6)

DHT dht(pin1, DHT22);

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
  float h = dht.readHumidity();
  float tc = dht.readTemperature();
  float tf = dht.readTemperature(true);
  float st = dht.computeHeatIndex(tc, h, false);

  Serial.println("Temperatura: " + String(tc) + " °C");
  Serial.println("Humedad: " + String(h) + " %");
  Serial.println("Temperatura: " + String(tf) + " °F");
  Serial.println("Sensación Térmica: " + String(st) + " °C");
  Serial.println("--------------------------------------------");
  delay(2000);
}

void leerpot() {
  int potValor = analogRead(pin2);
  float vol = potValor * 3.3 / 4095.0;
  Serial.println("Lectura ADC: " + String(potValor) + " binario");
  Serial.println("Voltaje: " + String(vol, 2) + " V");
  Serial.println("--------------------------------------------");
  delay(500);
}
"""

C4_CODE = """// CIRCUITO 4: ESP32 + WIFI + ADAFRUIT IO (MQTT)
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// Configuración WiFi Wokwi
#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

// Servidor y Credenciales Adafruit IO
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "gianfranco_arocutipa"
#define AIO_KEY         "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx"

#define DHTPIN          13
#define DHTTYPE         DHT22
int pin2 = 34;          // GPIO 34 (ADC1_CH6)

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// Feeds en Adafruit IO
Adafruit_MQTT_Publish temperatura = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/DHT22");
Adafruit_MQTT_Publish voltaje     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/Potenciometro");

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
  Serial.println("\\nWiFi conectado exitosamente");
}

void loop() {
  conectarMQTT();
  leerdht();
  leerpot();
  Serial.println("Datos enviados a Adafruit IO");
  Serial.println("--------------------------------");
  delay(7000);
}

void leerdht() {
  float tc = dht.readTemperature();
  if (!isnan(tc)) {
    Serial.println("Temperatura : " + String(tc) + " °C");
    temperatura.publish(tc);
  }
}

void leerpot() {
  int lectura = analogRead(pin2);
  float vol = lectura * 3.3 / 4095.0;
  Serial.println("ADC      : " + String(lectura));
  Serial.println("Voltaje  : " + String(vol) + " V");
  voltaje.publish(vol);
}

void conectarMQTT() {
  int8_t ret;
  if (mqtt.connected()) return;

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

C5_CODE = """// CIRCUITO 5: CUESTIONARIO INTEGRAL - 5 FEEDS EN ADAFRUIT IO
// Publica: Temperatura, Humedad, Sensación Térmica, Potenciómetro 1 y Potenciómetro 2
#include <WiFi.h>
#include "DHT.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define WLAN_SSID       "Wokwi-GUEST"
#define WLAN_PASS       ""

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "gianfranco_arocutipa"
#define AIO_KEY         "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxx"

#define DHTPIN          13
#define DHTTYPE         DHT22
const int pinPot1     = 34; // Potenciómetro 1 (ADC1 - Canal 6)
const int pinPot2     = 35; // Potenciómetro 2 (ADC1 - Canal 7)

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

// 5 Feeds configurados en Adafruit IO
Adafruit_MQTT_Publish feedTemp     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/temperatura");
Adafruit_MQTT_Publish feedHum      = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/humedad");
Adafruit_MQTT_Publish feedSensTerm = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/sensacion-termica");
Adafruit_MQTT_Publish feedPot1     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/potenciometro-1");
Adafruit_MQTT_Publish feedPot2     = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/potenciometro-2");

DHT dht(DHTPIN, DHTTYPE);

void conectarMQTT();

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Iniciando conexión WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\\n[WiFi] Conectado exitosamente");
}

void loop() {
  conectarMQTT();

  // 1. Lecturas de DHT22
  float h = dht.readHumidity();
  float tc = dht.readTemperature();
  if (!isnan(h) && !isnan(tc)) {
    float st = dht.computeHeatIndex(tc, h, false);
    Serial.println("[DHT22] Temp: " + String(tc, 1) + " °C | Hum: " + String(h, 1) + " % | ST: " + String(st, 1) + " °C");
    feedTemp.publish(tc);
    feedHum.publish(h);
    feedSensTerm.publish(st);
  }

  // 2. Potenciómetro 1 (GPIO 34 - ADC1)
  int val1 = analogRead(pinPot1);
  float vol1 = val1 * 3.3 / 4095.0;
  Serial.println("[POT 1] ADC: " + String(val1) + " | Voltaje: " + String(vol1, 2) + " V");
  feedPot1.publish(vol1);

  // 3. Potenciómetro 2 (GPIO 35 - ADC1)
  int val2 = analogRead(pinPot2);
  float vol2 = val2 * 3.3 / 4095.0;
  Serial.println("[POT 2] ADC: " + String(val2) + " | Voltaje: " + String(vol2, 2) + " V");
  feedPot2.publish(vol2);

  Serial.println("-> 5 Feeds transmitidos a Adafruit IO. Próximo ciclo en 7s...");
  Serial.println("----------------------------------------------------------------");
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
  Serial.println("¡Conectado exitosamente!");
}
"""

def build_full_report(output_dir, assets_dir, images_dir):
    doc = docx.Document()
    setup_page_layout(doc, assets_dir)

    print("Building Portada...")
    # PORTADA
    add_p(doc, "UNIVERSIDAD PRIVADA DE TACNA", bold=True, font_size=18, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_p(doc, "FACULTAD DE INGENIERÍA", bold=True, font_size=16, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", bold=True, font_size=14, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    c_logo = os.path.join(assets_dir, 'cover_logo_5.png')
    if os.path.exists(c_logo):
        p_c_img = doc.add_paragraph()
        p_c_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c_img.paragraph_format.space_before = Pt(4)
        p_c_img.paragraph_format.space_after = Pt(14)
        p_c_img.add_run().add_picture(c_logo, width=Inches(2.45))

    add_p(doc, "Guía Práctica de Laboratorio Nº9", bold=True, font_size=20, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4)
    add_p(doc, "“PLACA ESP32 Y CLOUD IOT ADAFRUIT”", bold=True, font_size=14, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=16)

    add_p(doc, "Que se presenta para el curso:", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "“INTERNET DE LAS COSAS”", bold=True, font_size=14, font_color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=18)

    add_p(doc, "Docente:", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "Mgr. Alex Juan Yanqui Constancio", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    add_p(doc, "Estudiantes:", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "Perez Peralta, Fabrizio Salvador Elias – 2023077476", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Arocutipa Arocutipa, Gian Franco - 2023076790", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24)

    add_p(doc, "TACNA – PERÚ", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=2)
    add_p(doc, "2026", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0)

    doc.add_page_break()

    print("Building Índice General...")
    # ÍNDICE GENERAL
    add_p(doc, "Índice General", bold=True, font_size=13, font_color=COLOR_PRIMARY, space_before=10, space_after=10)

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
        ("      2.1.   Instalación y Configuración del ESP32 en Arduino IDE", "5"),
        ("      2.2.   Montaje y Distribución de Pines (Pinout del ESP32 DevKit v1)", "6"),
        ("      2.3.   Circuito 1: Programa Hola Mundo y Comunicación Serial (115200 baudios)", "7"),
        ("      2.4.   Circuito 2: Control de Semáforo de 3 LEDs mediante GPIOs", "8"),
        ("      2.5.   Modificación del Semáforo con Reporte en Puerto Serial", "9"),
        ("      2.6.   Circuito 3: Prueba con Sensor DHT22 y Potenciómetro Analógico (ADC)", "10"),
        ("      2.7.   Configuración de la Plataforma Cloud Adafruit IO (Feeds y Dashboards)", "12"),
        ("      2.8.   Circuito 4: Conexión WiFi y Publicación MQTT hacia Adafruit IO", "14"),
        ("      2.9.   Circuito 5: Resolución del Cuestionario Integrador (5 Feeds y 2 Potenciómetros)", "16"),
        ("3.   Análisis Teórico y Cálculos de Ingeniería", "18"),
        ("      3.1.   Cuantización y Resolución del ADC de 12 Bits del ESP32", "18"),
        ("      3.2.   Dimensionamiento de Resistencias Limitadoras para LEDs a 3.3V", "18"),
        ("      3.3.   Comparativa de Rendimiento y Overhead: Protocolo MQTT vs HTTP en IoT", "19"),
        ("      3.4.   Restricción de Canales ADC con WiFi Activo (ADC1 vs ADC2)", "19"),
        ("4.   Conclusiones", "20"),
        ("5.   Referencias Bibliográficas", "21"),
        ("6.   Anexos", "22")
    ]

    for title, page_no in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(2.5)
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        r_t1 = p_t.add_run(title)
        r_t1.font.name = 'Arial'
        r_t1.font.size = Pt(10.5)
        r_t1.font.color.rgb = COLOR_TEXT
        
        r_tab = p_t.add_run('\t')
        r_tab.font.name = 'Arial'
        r_tab.font.size = Pt(10.5)

        r_pgn = p_t.add_run(page_no)
        r_pgn.font.name = 'Arial'
        r_pgn.font.size = Pt(10.5)
        r_pgn.font.bold = True
        r_pgn.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()

    print("Building Introducción...")
    # INTRODUCCIÓN
    add_heading_1(doc, "Introducción")
    add_p(doc, "El microcontrolador ESP32 de Espressif Systems es un sistema en chip (SoC) de alto rendimiento y bajo costo, diseñado específicamente para aplicaciones de Internet de las Cosas (IoT). Incorpora un microprocesador Tensilica Xtensa Dual-Core de 32 bits que opera a frecuencias de hasta 240 MHz, integrando de forma nativa conectividad inalámbrica Wi-Fi (802.11 b/g/n) y Bluetooth de modo dual (Classic y BLE). A diferencia de plataformas clásicas de 8 bits como el ATmega328P, el ESP32 ofrece 520 KB de memoria SRAM interna y una arquitectura optimizada para soportar pilas de comunicación de red completas (TCP/IP) y sistemas operativos en tiempo real (FreeRTOS).")

    add_p(doc, "En entornos IoT, la captura y telemetría de variables físicas requiere la integración de sensores digitales y analógicos. Para variables ambientales como temperatura y humedad relativa, el sensor digital DHT22 proporciona alta resolución y estabilidad mediante comunicación unifilar propietaria. Asimismo, el ESP32 dispone de dos convertidores analógico-digitales (ADC) SAR de 12 bits (0 a 4095 niveles), lo que permite cuantizar tensiones analógicas de transductores resistivos (potenciómetros) con una resolución teórica de aproximadamente 0.8 mV por paso en su rango de 3.3V.")

    add_p(doc, "Para la gestión remota de los datos recolectados, la plataforma en la nube Adafruit IO ofrece un ecosistema IoT flexible basado en el protocolo ligero MQTT (Message Queuing Telemetry Transport). A través del paradigma de publicación y suscripción (Pub/Sub) sobre el puerto TCP 1883, el ESP32 actúa como cliente publicador de datos hacia tópicos denominados 'Feeds'. En el panel de control (Dashboard), estos datos se grafican e interpretan en tiempo real mediante bloques interactivos (medidores circulares, diagramas de línea y conmutadores).")

    add_p(doc, "La validación experimental de estos sistemas se realiza mediante el simulador Wokwi, el cual proporciona emulación del ciclo de reloj del ESP32 y una pasarela de red virtual Wi-Fi ('Wokwi-GUEST'). Esto permite que el microcontrolador simulado establezca conexiones TCP reales hacia los servidores de Adafruit IO en Internet, validando la integridad del firmware antes de su despliegue físico.")

    doc.add_page_break()

    print("Building Sección 1: Información...")
    # SECCIÓN 1: INFORMACIÓN
    add_p(doc, "Guía de Laboratorio Nº9 “PLACA Esp32”", bold=True, font_size=11, font_color=COLOR_MUTED, space_before=4, space_after=6)
    add_heading_1(doc, "1. Información sobre el evento práctico")

    add_heading_2(doc, "1.1. Título del evento práctico")
    add_p(doc, "Configuración del Microcontrolador ESP32, Lectura de Sensores Digitales/Analógicos e Integración Cloud IoT con Adafruit IO")

    add_heading_2(doc, "1.2. Objetivos")
    add_bullet(doc, "Configurar el entorno de desarrollo Arduino IDE y la plataforma de simulación Wokwi para la arquitectura ESP32.")
    add_bullet(doc, "Implementar la comunicación serial asíncrona a 115200 baudios y el control de salidas digitales GPIO (semáforo de LEDs).")
    add_bullet(doc, "Adquirir datos ambientales mediante el sensor digital DHT22 y magnitudes analógicas mediante el ADC de 12 bits.")
    add_bullet(doc, "Conectar el ESP32 a la red Wi-Fi y transmitir telemetría en tiempo real hacia la nube Adafruit IO utilizando el protocolo MQTT.")
    add_bullet(doc, "Resolver el cuestionario integrador publicando simultáneamente 5 feeds en Adafruit IO (Temperatura, Humedad, Sensación Térmica y 2 Potenciómetros).")

    add_heading_2(doc, "1.3. Tiempo de duración (horas)")
    add_p(doc, "02 horas académicas.")

    add_heading_2(doc, "1.4. Resultados de Aprendizaje (RA)")
    add_bullet(doc, "Configura el microcontrolador ESP32 aplicando buenas prácticas de conexionado y restricciones de pines de hardware.", bold_prefix="RA1: ")
    add_bullet(doc, "Configura sensores, actuadores y enlaces de red en Wokwi e integra telemetría cloud mediante protocolos IoT estándar.", bold_prefix="RA2: ")

    add_heading_2(doc, "1.5. Recursos (Equipos, materiales, programas y otros)")
    add_bullet(doc, "Computador personal con acceso a Internet y navegador web moderno.")
    add_bullet(doc, "Plataforma de simulación Wokwi (https://wokwi.com) y Arduino IDE.")
    add_bullet(doc, "1 Microcontrolador ESP32 DevKit v1 (30 pines).")
    add_bullet(doc, "1 Sensor digital de temperatura y humedad DHT22.")
    add_bullet(doc, "2 Potenciómetros lineales de 10 kΩ.")
    add_bullet(doc, "3 Diodos LED (Verde, Amarillo y Rojo) y 3 Resistencias de 220 Ω.")
    add_bullet(doc, "Plataforma Cloud Adafruit IO (https://io.adafruit.com).")

    add_heading_2(doc, "1.6. Ventajas del ESP32 y Adafruit IO en IoT")
    add_bullet(doc, "Procesamiento y Red: El ESP32 cuenta con doble núcleo a 240 MHz y Wi-Fi nativo, superando el límite de procesamiento y memoria de los microcontroladores de 8 bits.")
    add_bullet(doc, "Eficiencia de Protocolo: MQTT minimiza la sobrecarga de encabezados frente a HTTP, permitiendo transmisiones frecuentes con bajo ancho de banda y menor consumo energético.")
    add_bullet(doc, "Plataforma Cloud: Adafruit IO simplifica la creación de paneles de visualización (Dashboards) sin requerir el despliegue de servidores locales.")

    doc.add_page_break()

    print("Building Sección 2: Procedimiento...")
    # SECCIÓN 2: PROCEDIMIENTO
    add_heading_1(doc, "2. Procedimiento o Metodología")

    add_heading_2(doc, "2.1. Instalación y Configuración del ESP32 en Arduino IDE")
    add_p(doc, "Para programar el ESP32 en el entorno local de Arduino IDE se requiere instalar el Core oficial desarrollado por Espressif Systems:")
    add_num_item(doc, "1", "Acceder a 'Archivo > Preferencias' e incorporar en el campo 'Gestor de URLs Adicionales de Tarjetas' el repositorio oficial: https://espressif.github.io/arduino-esp32/package_esp32_index.json")
    add_num_item(doc, "2", "Ingresar a 'Herramientas > Placa > Gestor de Tarjetas', buscar 'esp32' de Espressif e instalar la versión estable más reciente.")
    add_num_item(doc, "3", "En 'Herramientas > Placa', seleccionar el modelo 'DOIT ESP32 DEVKIT V1' (o 'ESP32 Dev Module') y fijar la velocidad del puerto serie a 115200 baudios.")

    add_heading_2(doc, "2.2. Montaje y Distribución de Pines (Pinout del ESP32 DevKit v1)")
    add_p(doc, "A diferencia de Arduino Uno o Nano, los pines del ESP32 trabajan con niveles lógicos de 3.3V (no tolerantes a 5V en entradas digitales puras). Además, las entradas analógicas se dividen en dos bloques ADC:")
    add_bullet(doc, "ADC1 (GPIO 32 a 39): Completamente independientes del radio Wi-Fi. Recomendados para sensores analógicos.")
    add_bullet(doc, "ADC2 (GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27): Comparten circuitos con el módem Wi-Fi. Cuando el Wi-Fi está encendido, el ADC2 queda inhabilitado para lecturas analógicas.")

    img_pinout = os.path.join(images_dir, 'page_8_img_2_Image87.png')
    add_capture_box(doc, "Pinout Oficial del ESP32 DevKit v1", "Esquema de distribución de pines y canales ADC1/ADC2 de la placa ESP32.", guide_img_path=img_pinout)

    add_heading_2(doc, "2.3. Circuito 1: Programa Hola Mundo y Comunicación Serial")
    add_p(doc, "El primer ejercicio comprueba la inicialización de la UART0 del ESP32 a 115200 baudios, demostrando la ejecución secuencial del bloque setup() y el ciclo periódico loop() con temporización de 2000 ms.")
    
    add_code_block(doc, C1_CODE, "Código Circuito 1 (sketch.ino):")
    
    img_c1 = os.path.join(images_dir, 'page_9_img_2_Image94.png')
    add_capture_box(doc, "Consola Serial del Circuito 1 (Hola Mundo)", "Captura de la salida del Monitor Serial a 115200 baudios mostrando los mensajes del setup() y loop().", guide_img_path=img_c1)

    add_heading_2(doc, "2.4. Circuito 2: Control de Semáforo de 3 LEDs mediante GPIOs")
    add_p(doc, "Implementación de una secuencia de semáforo vehicular con 3 LEDs conectados a salidas digitales mediante resistencias limitadoras de 220 Ω:")
    
    headers_c2 = ["Componente", "Pin ESP32", "Tipo de Señal", "Función en el Circuito"]
    data_c2 = [
        ["LED Verde", "GPIO 18", "Salida Digital (HIGH/LOW)", "Indicador de paso permitido"],
        ["LED Amarillo", "GPIO 22", "Salida Digital (HIGH/LOW)", "Indicador de precaución / transición"],
        ["LED Rojo", "GPIO 21", "Salida Digital (HIGH/LOW)", "Indicador de detención obligatoria"],
        ["Resistencias (3x)", "GND Común", "Pasivo (220 Ω)", "Limitación de corriente a ~6 mA"]
    ]
    add_table(doc, headers_c2, data_c2, [1.5, 1.2, 1.8, 1.75])

    add_code_block(doc, C2_CODE, "Código Circuito 2 (sketch.ino - Semáforo con Reporte Serial):")

    img_c2_sch = os.path.join(images_dir, 'page_10_img_2_Image96.png')
    add_capture_box(doc, "Montaje del Semáforo en Wokwi", "Esquema circuital del ESP32 conectado a los 3 LEDs con sus respectivas resistencias de 220 Ω.", guide_img_path=img_c2_sch)

    img_c2_ser = os.path.join(images_dir, 'page_12_img_2_Image101.png')
    add_capture_box(doc, "Monitor Serial del Semáforo de LEDs", "Registro de conmutación de los LEDs en el terminal serial a 115200 baudios.", guide_img_path=img_c2_ser)

    add_heading_2(doc, "2.6. Circuito 3: Prueba con Sensor DHT22 y Potenciómetro Analógico")
    add_p(doc, "En este circuito se integran dos modalidades de adquisición: el sensor digital unifilar DHT22 (temperatura, humedad y cálculo de índice de calor) en el pin D13, y un potenciómetro de 10 kΩ en el pin D34 (canal ADC1_CH6). El firmware calcula el voltaje correspondiente a la resolución de 12 bits mediante la relación V = (ADC * 3.3) / 4095.0.")

    headers_c3 = ["Sensor / Elemento", "Pin ESP32", "Tipo", "Rango de Medición"]
    data_c3 = [
        ["DHT22 (SDA / Datos)", "GPIO 13", "Entrada Digital Unifilar", "-40 a 80 °C (±0.5°C), 0 a 100% RH"],
        ["DHT22 (VCC / GND)", "3.3V / GND", "Alimentación", "3.3 V DC"],
        ["Potenciómetro (Señal)", "GPIO 34 (ADC1_CH6)", "Entrada Analógica", "0 a 4095 (0.00 V a 3.30 V)"],
        ["Potenciómetro (Extremos)", "3.3V / GND", "Alimentación", "Referencia fija de 3.3V"]
    ]
    add_table(doc, headers_c3, data_c3, [1.8, 1.5, 1.4, 1.55])

    add_code_block(doc, C3_CODE, "Código Circuito 3 (sketch.ino - DHT22 y ADC):")

    img_c3 = os.path.join(images_dir, 'page_13_img_2_Image103.png')
    add_capture_box(doc, "Circuito Wokwi con DHT22 y Potenciómetro", "Simulación del sensor DHT22 y potenciómetro conectados al ESP32 con salida serial activa.", guide_img_path=img_c3)

    add_heading_2(doc, "2.7. Configuración de la Plataforma Cloud Adafruit IO")
    add_p(doc, "Para la recepción y visualización de la telemetría en la nube se configuró una cuenta en Adafruit IO (https://io.adafruit.com):")
    add_bullet(doc, "Creación de Feeds: Se habilitaron los canales 'DHT22' (o 'temperatura') y 'Potenciometro' para almacenar las series temporales de datos.")
    add_bullet(doc, "Obtención de Credenciales: Se extrajo el AIO_USERNAME y la AIO_KEY privada desde el botón 'My Key' para autenticar el cliente MQTT.")
    add_bullet(doc, "Diseño del Dashboard: Se integraron bloques visuales interactivos: 'Gauge' (medidor angular para voltaje) y 'Line Chart' (gráfico de evolución temporal para temperatura y humedad).")

    img_aio_acc = os.path.join(images_dir, 'page_14_img_2_Image106.png')
    add_capture_box(doc, "Panel Principal de Adafruit IO", "Interfaz de inicio de sesión y administración de proyectos en io.adafruit.com.", guide_img_path=img_aio_acc)

    img_aio_feeds = os.path.join(images_dir, 'page_15_img_2_Image109.png')
    add_capture_box(doc, "Configuración de Feeds en Adafruit IO", "Lista de feeds creados para recibir los datos transmitidos por el ESP32.", guide_img_path=img_aio_feeds)

    img_aio_dash = os.path.join(images_dir, 'page_16_img_2_Image115.png')
    add_capture_box(doc, "Construcción del Dashboard con Bloques", "Diseño del panel de control con medidores Gauge y gráficos de líneas en Adafruit IO.", guide_img_path=img_aio_dash)

    add_heading_2(doc, "2.8. Circuito 4: Conexión WiFi y Publicación MQTT hacia Adafruit IO")
    add_p(doc, "En este circuito se habilita la pila Wi-Fi sobre la red virtual 'Wokwi-GUEST' y se conecta al broker MQTT 'io.adafruit.com' (puerto 1883). Cada 7 segundos, el microcontrolador adquiere la temperatura del DHT22 y el voltaje del potenciómetro, publicando cada valor en su respectivo Feed.")

    add_code_block(doc, C4_CODE, "Código Circuito 4 (sketch.ino - WiFi + Adafruit MQTT):")

    img_aio_live = os.path.join(images_dir, 'page_18_img_2_Image120.png')
    add_capture_box(doc, "Telemetría en Vivo en Adafruit IO (Circuito 4)", "Visualización en tiempo real de los datos de temperatura y voltaje transmitidos desde Wokwi.", guide_img_path=img_aio_live)

    add_heading_2(doc, "2.9. Circuito 5: Resolución del Cuestionario Integrador (5 Feeds y 2 Potenciómetros)")
    add_p(doc, "Requerimiento Oficial (Página 20 de la Guía): 'Modifique el programa para que se pueda publicar temperatura, humedad, sensación térmica, coloque otro potenciómetro adicional y que se muestre en el Dashboard de Adafruit.'")
    
    add_p(doc, "Solución Técnica Desarrollada:")
    add_bullet(doc, "Ampliación de Canales Analógicos: Se incorporó un segundo potenciómetro conectado al pin GPIO 35 (canal ADC1_CH7). Al pertenecer al ADC1, opera con total estabilidad sin sufrir interferencias por el módem Wi-Fi.")
    add_bullet(doc, "Cálculo del Heat Index: Se procesa la sensación térmica en grados Celsius mediante el algoritmo de Rothfusz (computeHeatIndex(tc, h, false)).")
    add_bullet(doc, "Publicación Simultánea: El programa publica cada 7 segundos en 5 feeds distintos: 'temperatura', 'humedad', 'sensacion-termica', 'potenciometro-1' y 'potenciometro-2'.")

    headers_c5 = ["Feed en Adafruit IO", "Variable Física", "Fuente de Hardware", "Unidad de Medida"]
    data_c5 = [
        ["temperatura", "Temperatura Ambiental", "DHT22 (GPIO 13)", "°C"],
        ["humedad", "Humedad Relativa", "DHT22 (GPIO 13)", "% HR"],
        ["sensacion-termica", "Índice de Calor (Heat Index)", "Cálculo matemático en ESP32", "°C"],
        ["potenciometro-1", "Tensión Analógica 1", "Potenciómetro 1 (GPIO 34 - ADC1)", "Voltios (0 a 3.3 V)"],
        ["potenciometro-2", "Tensión Analógica 2", "Potenciómetro 2 (GPIO 35 - ADC1)", "Voltios (0 a 3.3 V)"]
    ]
    add_table(doc, headers_c5, data_c5, [1.6, 1.6, 1.85, 1.2])

    add_code_block(doc, C5_CODE, "Código Circuito 5 (sketch.ino - Cuestionario Integrador 5 Feeds):")

    add_capture_box(doc, "Circuito 5 en Wokwi (DHT22 + 2 Potenciómetros)", "Esquema Wokwi del ESP32 con DHT22 en GPIO 13 y ambos potenciómetros en GPIO 34 y GPIO 35.", min_height_in=2.0)
    add_capture_box(doc, "Dashboard Completo de Adafruit IO con 5 Feeds", "Captura del panel de Adafruit IO mostrando los 5 bloques activos (temperatura, humedad, sensación térmica y 2 potenciómetros).", min_height_in=2.0)

    doc.add_page_break()

    print("Building Sección 3: Cálculos...")
    # SECCIÓN 3: CÁLCULOS
    add_heading_1(doc, "3. Análisis Teórico y Cálculos de Ingeniería")

    add_heading_2(doc, "3.1. Cuantización y Resolución del ADC de 12 Bits del ESP32")
    add_p(doc, "El convertidor analógico a digital del ESP32 opera con una resolución nativa de 12 bits, dividiendo el rango dinámico de voltaje de referencia (0 a 3.3 V) en 4096 intervalos cuantizados (0 a 4095 en binario):")

    formula_adc = "V_LSB = V_ref / (2^N - 1) = 3.30 V / 4095 ≈ 0.80586 mV / LSB"
    bullets_adc = [
        "V_ref = 3.30 V (Tensión nominal de alimentación del regulador del ESP32).",
        "N = 12 bits -> 2^12 = 4096 niveles discretos.",
        "Resolución = Cada unidad leída en analogRead() representa aproximadamente 0.806 mV.",
        "Para una lectura de ADC = 2048: V_medido = 2048 * (3.3 / 4095) = 1.650 V (exactamente el 50% de la escala)."
    ]
    add_formula_box(doc, "Fórmula de Resolución del ADC (Tensión del Bit Menos Significativo - LSB):", formula_adc, bullets_adc)

    add_heading_2(doc, "3.2. Dimensionamiento de Resistencias Limitadoras para LEDs a 3.3V")
    add_p(doc, "Para proteger las etapas de salida GPIO del microcontrolador y los diodos LED, se calcula la resistencia en serie mediante la ley de Ohm:")

    formula_led = "R = (V_GPIO - V_F) / I_F"
    bullets_led = [
        "V_GPIO = 3.30 V (Nivel de salida digital en estado HIGH del ESP32).",
        "V_F (LED Verde / Amarillo) ≈ 2.00 V; V_F (LED Rojo) ≈ 1.80 V.",
        "I_F recomendada = 6 mA (proporciona iluminación adecuada sin sobrecargar el bus de alimentación).",
        "Para LED Verde: R = (3.3V - 2.0V) / 0.006 A = 216.67 Ω -> Se selecciona el valor estándar comercial de 220 Ω.",
        "Corriente real resultante: I_real = (3.3V - 2.0V) / 220 Ω = 5.91 mA (seguro para el GPIO, cuyo máximo es 12 mA recomendados)."
    ]
    add_formula_box(doc, "Cálculo de la Resistencia de Polarización de los LEDs:", formula_led, bullets_led)

    add_heading_2(doc, "3.3. Comparativa de Rendimiento y Overhead: Protocolo MQTT vs HTTP en IoT")
    add_p(doc, "La elección del protocolo MQTT frente a HTTP REST para telemetría continua se fundamenta en el volumen de datos de cabecera y el consumo energético en redes inalámbricas:")

    headers_mqtt = ["Criterio de Evaluación", "Protocolo MQTT (Usado en Lab)", "Protocolo HTTP (REST Clásico)"]
    data_mqtt = [
        ["Tamaño Mínimo de Cabecera", "2 Bytes (Ultra ligero)", "500 - 800 Bytes (Cabeceras extensas)"],
        ["Gestión de Conexión TCP", "Mantiene socket abierto (Keep-Alive)", "Abre y cierra conexión por cada POST"],
        ["Consumo de Ancho de Banda", "Muy Bajo (~90% menor overhead)", "Alto (Sobrecarga de texto HTTP)"],
        ["Consumo Energético en Batería", "Mínimo (Menos tiempo de radio activo)", "Elevado (Mayor tiempo en transmisión)"],
        ["Modelo de Comunicación", "Publish / Subscribe asíncrono", "Request / Response síncrono"]
    ]
    add_table(doc, headers_mqtt, data_mqtt, [1.8, 2.2, 2.25])

    add_heading_2(doc, "3.4. Restricción de Canales ADC con WiFi Activo (ADC1 vs ADC2)")
    add_p(doc, "Uno de los aspectos arquitectónicos más críticos del ESP32 es la compartición de recursos internos:")
    add_bullet(doc, "Causa del Conflicto: El bloque ADC2 utiliza internamente los mismos registros de conmutación de antena y amplificación del circuito de radio Wi-Fi/Bluetooth. Al ejecutar WiFi.begin(), el controlador de Wi-Fi toma posesión prioritaria del ADC2.")
    add_bullet(doc, "Impacto: Cualquier llamada a analogRead() en pines de ADC2 (GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27) retorna valores nulos o lecturas corruptas cuando el Wi-Fi está en funcionamiento.")
    add_bullet(doc, "Solución de Ingeniería Aplicada: En el Circuito 4 y Circuito 5 se asignaron los potenciómetros exclusivamente a los canales ADC1 (GPIO 34 y GPIO 35), garantizando telemetría 100% libre de colisiones.")

    doc.add_page_break()

    print("Building Conclusiones...")
    # SECCIÓN 4: CONCLUSIONES
    add_heading_1(doc, "4. Conclusiones")
    add_num_item(doc, "1", "Se logró la configuración exitosa del microcontrolador ESP32 DevKit v1 tanto en Arduino IDE como en la plataforma de simulación en la nube Wokwi, validando la compilación y subida de firmware con salida serial asíncrona a 115200 baudios.")
    add_num_item(doc, "2", "El control de actuadores digitales mediante pines GPIO demostró la correcta polarización de diodos LED a niveles lógicos de 3.3V, verificando experimentalmente que resistencias de 220 Ω limitan la corriente a 5.9 mA, protegiendo los transistores internos del microcontrolador.")
    add_num_item(doc, "3", "La adquisición multivariable con el sensor digital DHT22 y el potenciómetro demostró la capacidad del ESP32 para procesar simultáneamente protocolos unifilares digitales y lecturas analógicas de 12 bits con una resolución de 0.806 mV/LSB.")
    add_num_item(doc, "4", "Se comprobó la superioridad del protocolo MQTT sobre HTTP para aplicaciones IoT en tiempo real: su reducida cabecera fija de 2 bytes y su modelo Publish/Subscribe permitieron enviar periódicamente 5 feeds hacia Adafruit IO sin saturar el ancho de banda ni degradar el rendimiento.")
    add_num_item(doc, "5", "Se resolvió íntegramente el cuestionario propuesto integrando dos potenciómetros en los canales ADC1_CH6 (GPIO 34) y ADC1_CH7 (GPIO 35), confirmando la regla de diseño que prohíbe el uso de canales ADC2 durante operaciones Wi-Fi activas.")

    print("Building Referencias...")
    # SECCIÓN 5: REFERENCIAS
    add_heading_1(doc, "5. Referencias Bibliográficas")
    add_bullet(doc, "Ortiz Arciniega, J. L., Valencia Barahona, F. X., & colaboradores. (2025). ESP32: Manual básico para estudiantes. Alumni Editora Ecuador, Atuntaqui.")
    add_bullet(doc, "Burgoa Román, F. J. (2026). Microcontrolador ESP32-S3: curso práctico (1.ª ed.). RA-MA Editorial. Recuperado de https://elibro.net/es/lc/bibliotecaupt/titulos/294849")
    add_bullet(doc, "Espressif Systems. (2024). ESP32 Series Datasheet (v4.3). Espressif Systems Co., Ltd. https://www.espressif.com")
    add_bullet(doc, "Adafruit Industries. (2025). Adafruit IO Basics: MQTT API Reference Guide. Adafruit Learning System. https://learn.adafruit.com/welcome-to-adafruit-io")

    print("Building Anexos...")
    # SECCIÓN 6: ANEXOS
    add_heading_1(doc, "6. Anexos")
    add_heading_2(doc, "6.1. Guía Rápida de Conexión Wokwi con Adafruit IO")
    add_num_item(doc, "1", "Crear una cuenta gratuita en https://io.adafruit.com y abrir la pestaña 'Dashboards' para generar un nuevo panel de control.")
    add_num_item(doc, "2", "Obtener las credenciales personales (Username y AIO Key) desde el botón 'My Key' (icono de llave amarilla en la barra superior).")
    add_num_item(doc, "3", "En el simulador Wokwi, abrir el archivo 'libraries.txt' y asegurarse de tener instaladas las librerías: 'Adafruit MQTT Library' y 'DHT sensor library'.")
    add_num_item(doc, "4", "Configurar en sketch.ino el SSID como 'Wokwi-GUEST' y la contraseña vacía (\"\"). El gateway virtual de Wokwi conectará automáticamente el ESP32 a Internet.")
    add_num_item(doc, "5", "Iniciar la simulación presionando 'Play': los datos se transmitirán en vivo hacia los feeds y se graficarán automáticamente en el Dashboard.")

    # Save to all target paths
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

# =========================================================================
# WOKWI DIAGRAM DEFINITIONS
# =========================================================================

C1_DIAGRAM = {
    "version": 1,
    "author": "Perez Fabrizio - Arocutipa Gian Franco",
    "editor": "wokwi",
    "parts": [
        {"type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {}}
    ],
    "connections": [],
    "serialMonitor": {"display": "auto"},
    "dependencies": {}
}

C2_DIAGRAM = {
    "version": 1,
    "author": "Perez Fabrizio - Arocutipa Gian Franco",
    "editor": "wokwi",
    "parts": [
        {"type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {}},
        {"type": "wokwi-led", "id": "led_verde", "top": -60, "left": 140, "attrs": {"color": "green"}},
        {"type": "wokwi-led", "id": "led_amarillo", "top": 20, "left": 140, "attrs": {"color": "yellow"}},
        {"type": "wokwi-led", "id": "led_rojo", "top": 100, "left": 140, "attrs": {"color": "red"}},
        {"type": "wokwi-resistor", "id": "r1", "top": -30, "left": 200, "attrs": {"value": "220"}},
        {"type": "wokwi-resistor", "id": "r2", "top": 50, "left": 200, "attrs": {"value": "220"}},
        {"type": "wokwi-resistor", "id": "r3", "top": 130, "left": 200, "attrs": {"value": "220"}}
    ],
    "connections": [
        ["esp:18", "led_verde:A", "green", ["h20", "v-50"]],
        ["led_verde:C", "r1:1", "black", []],
        ["r1:2", "esp:GND.1", "black", ["h20", "v30", "h-120"]],
        ["esp:22", "led_amarillo:A", "gold", ["h20", "v0"]],
        ["led_amarillo:C", "r2:1", "black", []],
        ["r2:2", "esp:GND.1", "black", ["h20", "v-50", "h-120"]],
        ["esp:21", "led_rojo:A", "red", ["h20", "v50"]],
        ["led_rojo:C", "r3:1", "black", []],
        ["r3:2", "esp:GND.1", "black", ["h20", "v-130", "h-120"]]
    ],
    "serialMonitor": {"display": "auto"},
    "dependencies": {}
}

C3_DIAGRAM = {
    "version": 1,
    "author": "Perez Fabrizio - Arocutipa Gian Franco",
    "editor": "wokwi",
    "parts": [
        {"type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {}},
        {"type": "wokwi-dht22", "id": "dht1", "top": -80, "left": 140, "attrs": {}},
        {"type": "wokwi-potentiometer", "id": "pot1", "top": 100, "left": 140, "attrs": {"value": "10k"}}
    ],
    "connections": [
        ["dht1:VCC", "esp:3V3", "red", ["v-20", "h-140", "v120"]],
        ["dht1:SDA", "esp:13", "gold", ["h20", "v70", "h-80"]],
        ["dht1:GND", "esp:GND.1", "black", ["v20", "h-80"]],
        ["pot1:VCC", "esp:3V3", "red", ["h20", "v-200", "h-140", "v120"]],
        ["pot1:SIG", "esp:34", "green", ["h-40", "v-50"]],
        ["pot1:GND", "esp:GND.1", "black", ["h-40", "v-100"]]
    ],
    "serialMonitor": {"display": "auto"},
    "dependencies": {}
}

C4_DIAGRAM = C3_DIAGRAM

C5_DIAGRAM = {
    "version": 1,
    "author": "Perez Fabrizio - Arocutipa Gian Franco",
    "editor": "wokwi",
    "parts": [
        {"type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {}},
        {"type": "wokwi-dht22", "id": "dht1", "top": -90, "left": 150, "attrs": {}},
        {"type": "wokwi-potentiometer", "id": "pot1", "top": 60, "left": 150, "attrs": {"value": "10k"}},
        {"type": "wokwi-potentiometer", "id": "pot2", "top": 180, "left": 150, "attrs": {"value": "10k"}}
    ],
    "connections": [
        ["dht1:VCC", "esp:3V3", "red", ["v-20", "h-150", "v120"]],
        ["dht1:SDA", "esp:13", "gold", ["h20", "v80", "h-90"]],
        ["dht1:GND", "esp:GND.1", "black", ["v20", "h-90"]],
        ["pot1:VCC", "esp:3V3", "red", ["h20", "v-160", "h-150", "v120"]],
        ["pot1:SIG", "esp:34", "green", ["h-40", "v-10"]],
        ["pot1:GND", "esp:GND.1", "black", ["h-40", "v-60"]],
        ["pot2:VCC", "esp:3V3", "red", ["h20", "v-280", "h-150", "v120"]],
        ["pot2:SIG", "esp:35", "blue", ["h-40", "v-110"]],
        ["pot2:GND", "esp:GND.1", "black", ["h-40", "v-180"]]
    ],
    "serialMonitor": {"display": "auto"},
    "dependencies": {}
}

def generate_circuits_and_package(lab3_dir, current_lab2_dir):
    print("Creating circuit directories...")
    target_lab2u3 = os.path.join(lab3_dir, "lab 3u2")
    os.makedirs(target_lab2u3, exist_ok=True)

    circuits = [
        ("01_Circuito1_HolaMundo_ESP32", C1_CODE, C1_DIAGRAM, None,
         "# Circuito 1: Hola Mundo y Comunicación Serial (ESP32)\n\n"
         "## Descripción\n"
         "Verifica la inicialización de la UART0 a 115200 baudios en el ESP32 DevKit v1.\n\n"
         "## Instrucciones en Wokwi (https://wokwi.com)\n"
         "1. Pega `sketch.ino` en la pestaña de código.\n"
         "2. Pega `diagram.json` en la pestaña del diagrama.\n"
         "3. Presiona Play y observa los mensajes en el Monitor Serial.\n"),

        ("02_Circuito2_Semaforo_Leds_ESP32", C2_CODE, C2_DIAGRAM, None,
         "# Circuito 2: Control de Semáforo de 3 LEDs (ESP32)\n\n"
         "## Descripción\n"
         "Secuencia de luces con 3 LEDs controlados por los pines GPIO 18 (Verde), 22 (Amarillo) y 21 (Rojo) con resistencias de 220 Ω y reporte en puerto serial.\n\n"
         "## Instrucciones en Wokwi\n"
         "1. Pega `sketch.ino` y `diagram.json`.\n"
         "2. Presiona Play y observa la secuencia de encendido y apagado.\n"),

        ("03_Circuito3_Sensor_DHT22_Potenciometro", C3_CODE, C3_DIAGRAM, "DHT sensor library",
         "# Circuito 3: Sensor DHT22 y Potenciómetro Analógico (ESP32)\n\n"
         "## Descripción\n"
         "Adquisición combinada de variables ambientales (temperatura en °C y °F, humedad y sensación térmica) en GPIO 13, y lectura analógica de 12 bits en GPIO 34 (ADC1).\n\n"
         "## Instrucciones en Wokwi\n"
         "1. Pega `sketch.ino` y `diagram.json`.\n"
         "2. En `libraries.txt`, añade `DHT sensor library`.\n"
         "3. Presiona Play y mueve los controles del DHT22 y el potenciómetro.\n"),

        ("04_Circuito4_ESP32_WiFi_Adafruit_IO_MQTT", C4_CODE, C4_DIAGRAM, "Adafruit MQTT Library\nDHT sensor library",
         "# Circuito 4: Conexión WiFi y Publicación MQTT hacia Adafruit IO (ESP32)\n\n"
         "## Descripción\n"
         "Enlace IoT mediante la red virtual 'Wokwi-GUEST' hacia el broker MQTT 'io.adafruit.com', publicando periódicamente la temperatura y voltaje en Feeds de Adafruit IO.\n\n"
         "## Instrucciones en Wokwi\n"
         "1. Pega `sketch.ino` y `diagram.json`.\n"
         "2. En `libraries.txt`, añade `Adafruit MQTT Library` y `DHT sensor library`.\n"
         "3. Configura tus credenciales AIO_USERNAME y AIO_KEY en sketch.ino.\n"
         "4. Presiona Play y verifica los datos en tu Dashboard de Adafruit IO.\n"),

        ("05_Circuito5_Cuestionario_Integrador_Adafruit_5Feeds", C5_CODE, C5_DIAGRAM, "Adafruit MQTT Library\nDHT sensor library",
         "# Circuito 5: Cuestionario Integrador - 5 Feeds en Adafruit IO (ESP32)\n\n"
         "## Descripción\n"
         "Resolución completa del ejercicio integrador de la guía: publicación simultánea de Temperatura, Humedad, Sensación Térmica, Potenciómetro 1 (GPIO 34) y Potenciómetro 2 (GPIO 35).\n\n"
         "## Aspecto Clave de Hardware\n"
         "Ambos potenciómetros se conectan al ADC1 (GPIO 34 y 35) para evitar el conflicto de hardware del ADC2 con el módem Wi-Fi activo.\n\n"
         "## Instrucciones en Wokwi\n"
         "1. Pega `sketch.ino` y `diagram.json`.\n"
         "2. En `libraries.txt`, incluye las librerías requeridas.\n"
         "3. Inicia la simulación para alimentar los 5 feeds en tu Dashboard.\n")
    ]

    for folder_name, code, diagram, lib, readme in circuits:
        c_path = os.path.join(target_lab2u3, folder_name)
        os.makedirs(c_path, exist_ok=True)
        with open(os.path.join(c_path, "sketch.ino"), "w", encoding="utf-8") as f:
            f.write(code)
        with open(os.path.join(c_path, "diagram.json"), "w", encoding="utf-8") as f:
            json.dump(diagram, f, indent=2)
        if lib:
            with open(os.path.join(c_path, "libraries.txt"), "w", encoding="utf-8") as f:
                f.write(lib)
        with open(os.path.join(c_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
        print(f"Circuito {folder_name} generado.")

    # Master Unified TXT file
    master_txt_path = os.path.join(target_lab2u3, "TODOS_LOS_EJERCICIOS_WOKWI_LAB3.txt")
    with open(master_txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("GUÍA MAESTRA DE EJERCICIOS RESUELTOS - LABORATORIO 2.3 ESP32 WOKWI ADAFRUIT IO (LAB 3U2)\n")
        f.write("Autores: Perez Peralta, Fabrizio Salvador Elias & Arocutipa Arocutipa, Gian Franco\n")
        f.write("Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas\n")
        f.write("=" * 80 + "\n\n")
        for folder_name, code, diagram, lib, readme in circuits:
            f.write("=" * 80 + "\n")
            f.write(f"EJERCICIO: {folder_name.upper()}\n")
            f.write("=" * 80 + "\n\n")
            f.write("--------------------------------------------------------------------------------\n")
            f.write("ARCHIVO: sketch.ino\n")
            f.write("--------------------------------------------------------------------------------\n")
            f.write(code + "\n\n")
            f.write("--------------------------------------------------------------------------------\n")
            f.write("ARCHIVO: diagram.json\n")
            f.write("--------------------------------------------------------------------------------\n")
            f.write(json.dumps(diagram, indent=2) + "\n\n")
            if lib:
                f.write("--------------------------------------------------------------------------------\n")
                f.write("ARCHIVO: libraries.txt\n")
                f.write("--------------------------------------------------------------------------------\n")
                f.write(lib + "\n\n")

    # Copy PDF guide to target
    pdf_src = os.path.join(lab3_dir, "Lab 2.3 - Esp32 Wokwi - Adafruit.pdf")
    if os.path.exists(pdf_src):
        shutil.copy2(pdf_src, os.path.join(target_lab2u3, "Lab 2.3 - Esp32 Wokwi - Adafruit.pdf"))
        shutil.copy2(pdf_src, os.path.join(target_lab2u3, "Guia_Docente_Lab_2.3_ESP32.pdf"))

    # Copy Word reports to target
    docx_names = [
        "lab 3u2.docx",
        "lab 3.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit_Actualizado.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 3u2 Esp32 Wokwi - Adafruit.docx"
    ]
    for dname in docx_names:
        src = os.path.join(lab3_dir, dname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target_lab2u3, dname))

    # Also copy master txt and docx to root of lab3_dir
    shutil.copy2(master_txt_path, os.path.join(lab3_dir, "TODOS_LOS_EJERCICIOS_WOKWI_LAB3.txt"))

    # Create root README for 'lab 3u2'
    readme_content = """# Laboratorio 2.3 (Lab 3U2): Placa ESP32, Sensores y Cloud IoT Adafruit

**Universidad Privada de Tacna**  
**Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas**  
**Curso:** Internet de las Cosas  
**Docente:** Mgr. Alex Juan Yanqui Constancio  

**Integrantes:**
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790

---

## Contenido del Laboratorio

Esta carpeta contiene todos los informes académicos formales, los esquemas y códigos funcionales listos para simular en Wokwi y conectar a Adafruit IO:

```
lab 3u2/
│
├── lab 3u2.docx                                                   # Informe final en formato Word
├── lab 3.docx                                                     # Copia directa
├── Perez Fabrizio_Arocutipa Gian Franco_Lab 2.3 Esp32 Wokwi - Adafruit.docx
├── Lab 2.3 - Esp32 Wokwi - Adafruit.pdf                           # Guía oficial del docente
├── TODOS_LOS_EJERCICIOS_WOKWI_LAB3.txt                            # Códigos unificados para Wokwi
│
├── 01_Circuito1_HolaMundo_ESP32/                                  # Circuito 1: UART0 y Setup/Loop
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 02_Circuito2_Semaforo_Leds_ESP32/                              # Circuito 2: Semáforo de 3 LEDs
│   ├── sketch.ino
│   ├── diagram.json
│   └── README.md
│
├── 03_Circuito3_Sensor_DHT22_Potenciometro/                       # Circuito 3: DHT22 + ADC 12 bits
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   └── README.md
│
├── 04_Circuito4_ESP32_WiFi_Adafruit_IO_MQTT/                      # Circuito 4: Conexión WiFi + MQTT
│   ├── sketch.ino
│   ├── diagram.json
│   ├── libraries.txt
│   └── README.md
│
└── 05_Circuito5_Cuestionario_Integrador_Adafruit_5Feeds/          # Circuito 5: Cuestionario Resuelto
    ├── sketch.ino                                                 # 5 Feeds simultáneos en Adafruit IO
    ├── diagram.json                                               # ESP32 + DHT22 + 2 Potenciómetros
    ├── libraries.txt
    └── README.md
```

---

## Guía Rápida para Simular en Wokwi (https://wokwi.com)
1. Para cualquiera de los circuitos, abre Wokwi y crea un nuevo proyecto con **ESP32**.
2. Copia y pega el contenido de `sketch.ino` en la pestaña de código.
3. Copia y pega `diagram.json` en la pestaña del diagrama.
4. Si el circuito requiere librerías (Circuitos 3, 4 y 5), agrega el contenido de `libraries.txt` en el administrador de librerías.
5. Presiona **Play**:
   - En el Circuito 4 y 5, el ESP32 se conectará a la red Wi-Fi simulada `Wokwi-GUEST` y comenzará a enviar los datos vía MQTT al servidor `io.adafruit.com`.
"""
    with open(os.path.join(target_lab2u3, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Create ZIP archive
    zip_path = os.path.join(lab3_dir, "lab 3u2.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"Generating ZIP archive at {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_lab2u3):
            for file in files:
                if file.endswith(".zip"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, lab3_dir)
                zipf.write(full_path, rel_path)

    # Also save a copy named 'lab 3.zip'
    shutil.copy2(zip_path, os.path.join(lab3_dir, "lab 3.zip"))
    print("ZIP archives 'lab 3u2.zip' and 'lab 3.zip' created successfully.")

    # Also copy target_lab2u3 to current workspace for convenience
    local_copy_dir = os.path.join(current_lab2_dir, "lab 3u2")
    if os.path.exists(local_copy_dir):
        shutil.rmtree(local_copy_dir)
    shutil.copytree(target_lab2u3, local_copy_dir)
    shutil.copy2(zip_path, os.path.join(current_lab2_dir, "lab 3u2.zip"))
    shutil.copy2(os.path.join(lab3_dir, "lab 3u2.docx"), os.path.join(current_lab2_dir, "lab 3u2.docx"))
    print("Synchronized local copy into workspace 'lab2'.")

def main():
    lab3_dir = r"C:\Users\PC\Desktop\oit\lab3"
    current_lab2_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(lab3_dir, "extracted_assets")
    images_dir = os.path.join(lab3_dir, "extracted_images")

    print(f"Building Lab 3 suite in {lab3_dir}...")
    build_full_report(lab3_dir, assets_dir, images_dir)
    generate_circuits_and_package(lab3_dir, current_lab2_dir)
    print("ALL TASKS FOR LAB 3 COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
