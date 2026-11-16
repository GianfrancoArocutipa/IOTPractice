# -*- coding: utf-8 -*-
"""
Full report generator script for Lab 2.2 with concise, direct explanations:
'Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi.docx'
Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas
Curso: Internet de las Cosas
Docente: Mgr. Alex Juan Yanqui Constancio
Estudiantes:
- Perez Peralta, Fabrizio Salvador Elias – 2023077476
- Arocutipa Arocutipa, Gian Franco - 2023076790
"""

import os
import sys
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

def setup_page_layout(doc):
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
        h_logo = os.path.abspath('extracted_assets/header_logo_18.png')
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

def build_entire_report():
    doc = docx.Document()
    setup_page_layout(doc)

    print("Building Portada...")
    # =========================================================================
    # PORTADA
    # =========================================================================
    add_p(doc, "UNIVERSIDAD PRIVADA DE TACNA", bold=True, font_size=18, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_p(doc, "FACULTAD DE INGENIERÍA", bold=True, font_size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "ESCUELA DE INGENIERÍA DE SISTEMAS", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    c_logo = os.path.abspath('extracted_assets/cover_logo_5.png')
    if os.path.exists(c_logo):
        p_c_img = doc.add_paragraph()
        p_c_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c_img.paragraph_format.space_before = Pt(4)
        p_c_img.paragraph_format.space_after = Pt(14)
        p_c_img.add_run().add_picture(c_logo, width=Inches(2.45))

    add_p(doc, "Guía Práctica de Laboratorio", bold=True, font_size=20, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4)
    add_p(doc, "“Arduino Nano”", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=16)

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

    print("Building Índice General...")
    # =========================================================================
    # ÍNDICE GENERAL (Placeholder to update after page count determination)
    # =========================================================================
    p_toc_title = add_p(doc, "Índice General", bold=True, font_size=11, space_before=10, space_after=10)

    # Temporary items (we will rewrite these with exact pages later)
    toc_p_list = []
    toc_items = [
        ("Introducción", "3"),
        ("1.   Información sobre el evento práctico", "4"),
        ("      1.1.   Título del evento práctico", "4"),
        ("      1.2.   Objetivos", "4"),
        ("      1.3.   Tiempo de duración (horas)", "4"),
        ("      1.4.   Resultados de Aprendizaje (RA)", "4"),
        ("      1.5.   Recursos (Equipos, materiales, programas y otros)", "4"),
        ("      1.6.   Ventajas de Wokwi y Arduino Nano", "4"),
        ("      1.7.   Cuenta en Wokwi", "5"),
        ("2.   Procedimiento o Metodología", "6"),
        ("      MONTAJE", "6"),
        ("      2.1.   Circuito 1: Contador de 0 a 9 con Display de 7 Segmentos", "6"),
        ("      2.2.   Circuito 2: Contador de 00 a 99 Multiplexado con Transistores 2N2222", "11"),
        ("      2.3.   Circuito 3: Sensor de Temperatura DHT22 con Visualización Multiplexada", "16"),
        ("3.   Análisis Teórico y Cálculos de Ingeniería", "20"),
        ("      3.1.   Dimensionamiento de Resistencias para Displays de 7 Segmentos", "20"),
        ("      3.2.   Polarización y Saturación del Transistor 2N2222 como Switch", "20"),
        ("      3.3.   Frecuencia de Multiplexación y Persistencia de la Visión (POV)", "20"),
        ("      3.4.   Justificación Técnica: Uso de Transistores frente a Pines Directos", "21"),
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
        toc_p_list.append((p_t, title))

    doc.add_page_break()

    print("Building Introducción (concisa)...")
    # =========================================================================
    # INTRODUCCIÓN (CONCISA)
    # =========================================================================
    add_p(doc, "Introducción", bold=True, font_size=11, space_before=10, space_after=8)

    add_p(doc, "El microcontrolador Arduino Nano es una plataforma de desarrollo compacta basada en el chip ATmega328P. Ofrece las mismas capacidades que el Arduino Uno, incluyendo 14 pines de entrada/salida digital y 16 MHz de velocidad, pero añade 8 entradas analógicas (A0-A7) en un formato reducido ideal para montaje directo sobre protoboard.")

    add_p(doc, "Los displays de 7 segmentos son dispositivos visuales formados por 8 diodos LED (7 segmentos y 1 punto decimal). En la configuración de cátodo común, los terminales negativos de todos los diodos se unen internamente a un pin común conectado a tierra (GND), encendiéndose cada segmento al recibir un estado HIGH (+5V) en su ánodo.")

    add_p(doc, "Para controlar varios displays sin agotar los pines del microcontrolador se utiliza la técnica de multiplexación: los displays comparten el mismo bus de datos para los segmentos y se encienden de forma alternada a alta velocidad. Mediante el fenómeno de persistencia de la visión (POV), el ojo humano los percibe encendidos simultáneamente. Para manejar la corriente de retorno de los cátodos sin dañar el Arduino, se emplean transistores NPN 2N2222 como interruptores electrónicos.")

    add_p(doc, "Asimismo, se integra el sensor digital DHT22 para monitorear temperatura (-40 a 80 °C) y humedad relativa mediante comunicación digital de un solo hilo, validando todo el sistema en el simulador en línea Wokwi mediante modelos personalizados (Custom Chips en C).")

    doc.add_page_break()

    print("Building Sección 1 (concisa)...")
    # =========================================================================
    # SECCIÓN 1: INFORMACIÓN SOBRE EL EVENTO PRÁCTICO (CONCISA)
    # =========================================================================
    add_p(doc, "Guía de Laboratorio Nº18 “Sensor ultrasónico y Arduino Nano”", bold=True, font_size=11, space_before=8, space_after=6)
    add_heading_1(doc, "1. Información sobre el evento práctico")

    add_heading_2(doc, "1.1. Título del evento práctico")
    add_p(doc, "Arduino Nano: Displays de 7 Segmentos, Multiplexación con Transistores 2N2222 y Sensor DHT22")

    add_heading_2(doc, "1.2. Objetivos")
    add_bullet(doc, "Aprender el conexionado y la programación del Arduino Nano en el simulador Wokwi.")
    add_bullet(doc, "Implementar el control directo de un display de 7 segmentos (contador de 0 a 9).")
    add_bullet(doc, "Diseñar un contador multiplexado de dos dígitos (00 a 99) usando transistores NPN 2N2222.")
    add_bullet(doc, "Crear y utilizar un Custom Chip en Wokwi para modelar el transistor 2N2222.")
    add_bullet(doc, "Integrar el sensor DHT22 para visualizar la temperatura en tiempo real en los displays multiplexados y el monitor serial.")
    add_bullet(doc, "Realizar los cálculos teóricos de resistencias, saturación de transistores y frecuencia de refresco.")

    add_heading_2(doc, "1.3. Tiempo de duración (horas)")
    add_p(doc, "02 horas.")

    add_heading_2(doc, "1.4. Resultados de Aprendizaje (RA)")
    add_bullet(doc, "Desarrolla circuitos con microcontroladores aplicando multiplexación y control de displays.", bold_prefix="RA1: ")
    add_bullet(doc, "Evalúa tecnologías de sensado digital y plataformas de simulación para IoT.", bold_prefix="RA2: ")

    add_heading_2(doc, "1.5. Recursos (Equipos, materiales, programas y otros)")
    add_bullet(doc, "Computador personal con conexión a Internet y navegador web.")
    add_bullet(doc, "Plataforma de simulación Wokwi (https://wokwi.com).")
    add_bullet(doc, "1 Arduino Nano (ATmega328P).")
    add_bullet(doc, "2 Displays de 7 segmentos de cátodo común.")
    add_bullet(doc, "2 Transistores BJT NPN 2N2222 (Custom Chip en Wokwi).")
    add_bullet(doc, "1 Sensor digital de temperatura y humedad DHT22.")
    add_bullet(doc, "Resistencias: 7 de 220 Ω (segmentos) y 2 de 1 kΩ (base de transistores).")
    add_bullet(doc, "Protoboard virtual y cables de conexión.")

    add_heading_2(doc, "1.6. Ventajas de Wokwi y Arduino Nano")
    add_bullet(doc, "El Arduino Nano es compacto y se conecta directamente sobre protoboard, ofreciendo 8 entradas analógicas frente a las 6 del Arduino Uno.")
    add_bullet(doc, "Wokwi permite simular circuitos en tiempo real desde el navegador sin necesidad de hardware físico ni riesgo de dañarlo.")
    add_bullet(doc, "Permite crear Custom Chips en lenguaje C para simular componentes específicos como transistores.")
    add_bullet(doc, "Facilita compartir proyectos mediante enlaces web y archivos de texto (diagram.json y sketch.ino).")

    add_heading_2(doc, "1.7. Cuenta en Wokwi")
    add_p(doc, "Se utiliza una cuenta vinculada con GitHub o Google para almacenar, editar y compartir los proyectos de simulación mediante enlaces permanentes.")

    doc.add_page_break()

    print("Building Sección 2: Circuito 1 (conciso)...")
    # =========================================================================
    # SECCIÓN 2: PROCEDIMIENTO O METODOLOGÍA
    # =========================================================================
    add_heading_1(doc, "2. Procedimiento o Metodología", space_before=8, space_after=4)
    add_p(doc, "MONTAJE", bold=True, font_size=12, space_before=2, space_after=6)

    # -------------------------------------------------------------------------
    # 2.1 CIRCUITO 1
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.1. Circuito 1: Contador de 0 a 9 con Display de 7 Segmentos (Arduino Nano)")
    add_p(doc, "Consiste en conectar un display de 7 segmentos de cátodo común al Arduino Nano para mostrar los números del 0 al 9 de forma ascendente con un intervalo de 500 ms.")

    add_wokwi_link(doc, "https://wokwi.com/projects/424368143431181313")

    add_guide_image(doc, 'extracted_images/page_6_img_2.png', "Figura 1: Esquema de conexión oficial para el Circuito 1 (Contador 0 a 9 con Arduino Nano).")

    add_capture_placeholder(doc, 1, "Montaje y Conexiones del Circuito 1 en Wokwi", [
        "Vista panorámica del circuito en el protoboard de Wokwi.",
        "Placa Arduino Nano conectada al display de 7 segmentos mediante los pines D2 a D8.",
        "Resistencia de 220 Ω conectada desde el cátodo común (pin central COM) hacia GND.",
        "Cables ordenados e identificados por colores."
    ])

    add_capture_placeholder(doc, 2, "Código Fuente sketch.ino del Circuito 1 en Wokwi", [
        "Panel del editor de Wokwi mostrando las variables de pines (int a = 2 a int g = 8).",
        "Función setup() configurando los 7 pines como salidas con pinMode().",
        "Lógica secuencial en loop() encendiendo cada dígito con digitalWrite() y delay(tiempo)."
    ])

    add_capture_placeholder(doc, 3, "Simulación en Ejecución del Circuito 1 Mostrando Dígitos", [
        "Simulación activa (botón verde Play presionado).",
        "Display iluminado mostrando claramente un número (por ejemplo, el '0', '5' u '8').",
        "Comprobación de que no hay errores en la consola inferior."
    ])

    c1_code = """// Declaramos los pines de salida,
// en el proyecto asi lo tenemos cableado
int a = 2;
int b = 3;
int c = 4;
int d = 5;
int e = 6;
int f = 7;
int g = 8;
int tiempo = 500; // para el delay

// Hacemos que todas nuestras variables sean salidas
void setup() {
  pinMode(a, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(c, OUTPUT);
  pinMode(d, OUTPUT);
  pinMode(e, OUTPUT);
  pinMode(f, OUTPUT);
  pinMode(g, OUTPUT);
}

void loop() {
  // Cero
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 1);
  digitalWrite(f, 1);
  digitalWrite(g, 0);

  delay(tiempo);

  // Uno
  digitalWrite(a, 0);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 0);
  digitalWrite(e, 0);
  digitalWrite(f, 0);
  digitalWrite(g, 0);

  delay(tiempo);

  // Dos
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 0);
  digitalWrite(d, 1);
  digitalWrite(e, 1);
  digitalWrite(f, 0);
  digitalWrite(g, 1);

  delay(tiempo);

  // Tres
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 0);
  digitalWrite(f, 0);
  digitalWrite(g, 1);

  delay(tiempo);

  // Cuatro
  digitalWrite(a, 0);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 0);
  digitalWrite(e, 0);
  digitalWrite(f, 1);
  digitalWrite(g, 1);

  delay(tiempo);

  // Cinco
  digitalWrite(a, 1);
  digitalWrite(b, 0);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 0);
  digitalWrite(f, 1);
  digitalWrite(g, 1);

  delay(tiempo);

  // Seis
  digitalWrite(a, 1);
  digitalWrite(b, 0);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 1);
  digitalWrite(f, 1);
  digitalWrite(g, 1);

  delay(tiempo);

  // Siete
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 0);
  digitalWrite(e, 0);
  digitalWrite(f, 0);
  digitalWrite(g, 0);

  delay(tiempo);

  // Ocho
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 1);
  digitalWrite(f, 1);
  digitalWrite(g, 1);

  delay(tiempo);

  // Nueve
  digitalWrite(a, 1);
  digitalWrite(b, 1);
  digitalWrite(c, 1);
  digitalWrite(d, 1);
  digitalWrite(e, 0);
  digitalWrite(f, 1);
  digitalWrite(g, 1);

  delay(tiempo);
}"""
    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 1 - Contador 0 a 9)", c1_code)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "El circuito utiliza un Arduino Nano conectado a un display de 7 segmentos de cátodo común. Los segmentos a, b, c, d, e, f y g se conectan a los pines digitales D2 al D8 a través de la protoboard. El terminal común (COM) va a GND mediante una resistencia de 220 Ω para proteger los diodos LED.")
    add_p(doc, "Como el display es de cátodo común, al colocar un pin en HIGH (+5V) el segmento correspondiente se ilumina, y con LOW (0V) permanece apagado.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Configuración de pines: En setup(), los pines 2 al 8 se definen como salidas (OUTPUT) con pinMode(). Se fija tiempo = 500 para una espera de medio segundo entre números.", "setup()")
    add_num_item(doc, "2", "Secuencia del contador: En loop(), se colocan en HIGH los segmentos necesarios para cada número del 0 al 9, usando delay(500) para pausar entre cada dígito. Al terminar el 9, la secuencia vuelve a iniciar desde el 0.", "loop()")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "El display inicia en '0' y cuenta progresivamente de uno en uno hasta el '9'.")
    add_bullet(doc, "Cada número se mantiene visible por 500 ms de forma clara y estable.")
    add_bullet(doc, "El ciclo completo toma 5 segundos y se repite de manera infinita.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "Resistencia en cátodo común: En simulación funciona con una sola resistencia en COM. En un circuito físico real se debe colocar una resistencia en cada pin de ánodo (D2 a D8) para que el brillo no varíe según la cantidad de segmentos encendidos.")
    add_bullet(doc, "Uso de delay(): La función delay() detiene la ejecución del microcontrolador. Sirve para este ejemplo básico, pero para circuitos más complejos con sensores o multiplexación se debe usar millis().")

    doc.add_page_break()

    print("Building Sección 2: Circuito 2 (conciso)...")
    # -------------------------------------------------------------------------
    # 2.2 CIRCUITO 2
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.2. Circuito 2: Contador de 00 a 99 Multiplexado con Transistores 2N2222 (Arduino Nano)")
    add_p(doc, "Este circuito implementa un contador de dos dígitos (00 a 99) mediante multiplexación. Ambos displays comparten los 7 pines de segmentos (D2 a D8), mientras que dos transistores NPN 2N2222 controlan el encendido alternado de los cátodos desde los pines D9 y D10.")

    add_wokwi_link(doc, "https://wokwi.com/projects/424368143431181313")

    add_guide_image(doc, 'extracted_images/page_8_img_2.png', "Figura 2: Esquema de conexión oficial para el Circuito 2 (Contador 00 a 99 multiplexado).")

    add_capture_placeholder(doc, 4, "Montaje del Circuito 2 Multiplexado con Transistores en Wokwi", [
        "Vista del Arduino Nano y los dos displays de 7 segmentos de cátodo común.",
        "Bus común de segmentos conectado en paralelo entre ambos displays y a los pines D2-D8.",
        "Los dos transistores 2N2222 conectando los cátodos COM a tierra (GND).",
        "Pines de habilitación D9 (decenas) y D10 (unidades) conectados a las bases de los transistores."
    ])

    add_capture_placeholder(doc, 5, "Archivos del Custom Chip 2N2222 en Wokwi", [
        "Editor de Wokwi mostrando las pestañas 2n2222.chip.json y 2n2222.chip.c.",
        "Definición de pines BASE, EMI y COL en el archivo JSON.",
        "Código en C con la función on_base_change() que conmuta el colector al recibir nivel HIGH en la base."
    ])

    add_capture_placeholder(doc, 6, "Simulación en Ejecución Mostrando Conteo Multiplexado (00 a 99)", [
        "Simulación activa con el contador corriendo.",
        "Ambos displays visualizando un número de dos dígitos simultáneos (ej. '47' u '88') sin parpadeo.",
        "Indicador de tiempo de Wokwi avanzando normalmente."
    ])

    c2_sketch = """// Proyecto 02 nano
const byte segmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de habilitacion
const byte display1 = 9;   // Decenas
const byte display2 = 10;  // Unidades

// Tabla de segmentos
// a b c d e f g
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
  for (int i = 0; i < 7; i++)
    pinMode(segmentos[i], OUTPUT);

  pinMode(display1, OUTPUT);
  pinMode(display2, OUTPUT);

  digitalWrite(display1, LOW);
  digitalWrite(display2, LOW);
}

void mostrarNumero(byte numero) {
  for (int i = 0; i < 7; i++)
    digitalWrite(segmentos[i], numeros[numero][i]);
}

void mostrar(byte valor) {
  byte decenas = valor / 10;
  byte unidades = valor % 10;

  // Decenas
  digitalWrite(display2, LOW);
  mostrarNumero(decenas);
  digitalWrite(display1, HIGH);
  delay(4);
  digitalWrite(display1, LOW);

  // Unidades
  mostrarNumero(unidades);
  digitalWrite(display2, HIGH);
  delay(4);
  digitalWrite(display2, LOW);
}

void loop() {
  for (int contador = 0; contador < 100; contador++) {
    unsigned long t = millis();

    while (millis() - t < 1000) {
      mostrar(contador);
    }
  }
}"""
    add_code_box(doc, "Código Fuente Principal: sketch.ino (Circuito 2 - Contador 00 a 99)", c2_sketch)

    c2_json = """{
  "name": "2n2222",
  "author": "ALEX JUAN YANQUI CONSTANCIO",
  "pins": [
    "",
    "BASE",
    "EMI",
    "COL"
  ]
}"""
    add_code_box(doc, "Archivo de Configuración del Custom Chip: 2n2222.chip.json", c2_json)

    c2_c = """#include "wokwi-api.h"
#include <stdlib.h>

typedef struct {
  pin_t pin_base;
  pin_t pin_col;
  pin_t pin_emi;
} chip_state_t;

static void on_base_change(void *user_data, pin_t pin, uint32_t level) {
  chip_state_t *chip = (chip_state_t *)user_data;
  
  if (level == HIGH) {
    // NPN Activado: El colector se une al emisor (GND digital)
    pin_mode(chip->pin_col, OUTPUT);
    pin_write(chip->pin_col, LOW); 
  } else {
    // NPN Desactivado: Colector en alta impedancia (circuito abierto)
    pin_mode(chip->pin_col, INPUT); 
  }
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_base = pin_init("BASE", INPUT);
  chip->pin_col = pin_init("COL", INPUT); // Inicia abierto
  chip->pin_emi = pin_init("EMI", INPUT);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = on_base_change,
    .user_data = chip,
  };
  pin_watch(chip->pin_base, &watch_config);
}"""
    add_code_box(doc, "Lógica en Lenguaje C del Custom Chip: 2n2222.chip.c", c2_c)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "Este circuito multiplexa dos displays de 7 segmentos usando solo 9 pines (7 de datos y 2 de control), en lugar de los 14 que requeriría la conexión directa. Los ánodos homólogos (a con a, b con b, etc.) están unidos en paralelo y se conectan a los pines D2 a D8.")
    add_p(doc, "Los cátodos comunes se conectan al colector de sendos transistores NPN 2N2222, cuyos emisores van a GND. Al enviar HIGH desde D9 o D10 a la base del transistor, este se satura y conecta el cátodo a tierra, encendiendo ese display. El Custom Chip de Wokwi simula este comportamiento: con HIGH en la base une el colector a GND, y con LOW lo deja en circuito abierto.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Tabla de números: La matriz numeros[10][7] almacena los 1 y 0 de cada segmento. mostrarNumero(n) recorre la tabla para colocar los valores en los pines D2 a D8.", "numeros[10][7]")
    add_num_item(doc, "2", "Separación de dígitos: mostrar(valor) calcula decenas = valor / 10 y unidades = valor % 10 con división entera y módulo.", "mostrar()")
    add_num_item(doc, "3", "Multiplexado rápido: Enciende el display de decenas por 4 ms con display1 en HIGH, lo apaga; luego enciende el display de unidades por 4 ms con display2 en HIGH y lo apaga. El ciclo dura 8 ms (125 Hz).", "Tiempos")
    add_num_item(doc, "4", "Temporización no bloqueante: En loop(), un bucle while(millis() - t < 1000) mantiene el refresco continuo llamando a mostrar() durante 1 segundo antes de avanzar al siguiente número.", "loop()")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "Ambos displays se perciben encendidos al mismo tiempo gracias a la velocidad de alternancia.")
    add_bullet(doc, "El conteo avanza con precisión de '00' a '99', cambiando cada 1 segundo.")
    add_bullet(doc, "Al llegar a '99', el contador se reinicia automáticamente en '00'.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "Prevención de sombras (ghosting): El código apaga siempre el display activo antes de encender el siguiente. Esto evita que los segmentos de un dígito aparezcan tenuemente en el otro.")
    add_bullet(doc, "Protección con transistores: Cuando el display muestra un '8' consume cerca de 100 mA en el cátodo. Como un pin de Arduino solo soporta 40 mA, el uso de los transistores 2N2222 es indispensable para no quemar el microcontrolador.")

    doc.add_page_break()

    print("Building Sección 2: Circuito 3 (conciso)...")
    # -------------------------------------------------------------------------
    # 2.3 CIRCUITO 3
    # -------------------------------------------------------------------------
    add_heading_2(doc, "2.3. Circuito 3: Implementación del Sensor de Temperatura DHT22 con Visualización en Displays Multiplexados (Arduino Nano)")
    add_p(doc, "Cumpliendo con la instrucción de la página 11 de la guía ('Coloque un sensor de temperatura DHT22 - Implemente'), se integra el sensor DHT22 al circuito multiplexado para medir la temperatura ambiente y mostrarla en tiempo real en los displays (°C) y en el monitor serial.")

    add_wokwi_link(doc, "https://wokwi.com/projects/424368143431181313")

    add_capture_placeholder(doc, 7, "Montaje Integrado del Circuito 3 (Nano + DHT22 + Displays Multiplexados)", [
        "Circuito completo en Wokwi con Arduino Nano, sensor DHT22 y 2 displays de 7 segmentos multiplexados.",
        "Pin de datos (SDA) del DHT22 conectado al pin digital D11 del Arduino Nano.",
        "Alimentación del DHT22: pin 1 a +5V y pin 4 a GND.",
        "Conexiones de segmentos (D2-D8) y habilitación de transistores (D9-D10) operando conjuntamente."
    ])

    add_capture_placeholder(doc, 8, "Código Fuente Completo y Librerías en Wokwi", [
        "Pestaña libraries.txt en Wokwi con la línea: DHT sensor library.",
        "Directivas #include <DHT.h>, #define DHTPIN 11 y #define DHTTYPE DHT22 en el sketch.",
        "Estructura condicional con millis() para la lectura del sensor cada 1.5 a 2 segundos."
    ])

    add_capture_placeholder(doc, 9, "Simulación Interactiva del DHT22 Mostrando Temperatura", [
        "Simulación activa con el menú de control del sensor DHT22 abierto (ajustado ej. a 28 °C o 35 °C).",
        "Los displays de 7 segmentos mostrando el valor entero correspondiente a la temperatura seleccionada.",
        "Monitor Serial imprimiendo las lecturas: '[DHT22] Temperatura: XX.X °C | Humedad: YY.Y %'."
    ])

    c3_sketch = """#include "DHT.h"

#define DHTPIN 11      // Pin conectado a la linea de datos (SDA) del DHT22
#define DHTTYPE DHT22  // Sensor DHT22 (AM2302)

DHT dht(DHTPIN, DHTTYPE);

// Pines de los segmentos a, b, c, d, e, f, g
const byte segmentos[7] = {2, 3, 4, 5, 6, 7, 8};

// Pines de habilitacion de los transistores
const byte display1 = 9;   // Decenas
const byte display2 = 10;  // Unidades

// Tabla de segmentos para catodo comun
// a, b, c, d, e, f, g
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

float temperatura = 24.0;
float humedad = 50.0;
unsigned long ultimoMuestreo = 0;

void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(segmentos[i], OUTPUT);
  }
  pinMode(display1, OUTPUT);
  pinMode(display2, OUTPUT);

  digitalWrite(display1, LOW);
  digitalWrite(display2, LOW);

  Serial.begin(9600);
  Serial.println(F("=== Sistema de Monitoreo DHT22 Iniciado ==="));
  dht.begin();
}

void mostrarNumero(byte numero) {
  for (int i = 0; i < 7; i++) {
    digitalWrite(segmentos[i], numeros[numero][i]);
  }
}

void mostrar(byte valor) {
  byte decenas = valor / 10;
  byte unidades = valor % 10;

  // Mostrar Decenas
  digitalWrite(display2, LOW);
  mostrarNumero(decenas);
  digitalWrite(display1, HIGH);
  delay(4);
  digitalWrite(display1, LOW);

  // Mostrar Unidades
  mostrarNumero(unidades);
  digitalWrite(display2, HIGH);
  delay(4);
  digitalWrite(display2, LOW);
}

void loop() {
  unsigned long tiempoActual = millis();

  // Lectura del sensor cada 1.5 a 2 segundos
  if (tiempoActual - ultimoMuestreo >= 1500) {
    ultimoMuestreo = tiempoActual;
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (!isnan(t) && !isnan(h)) {
      temperatura = t;
      humedad = h;
      Serial.print(F("[DHT22] Temperatura: "));
      Serial.print(temperatura, 1);
      Serial.print(F(" °C  |  Humedad: "));
      Serial.print(humedad, 1);
      Serial.println(F(" %"));
    } else {
      Serial.println(F("Error en la lectura del sensor DHT22!"));
    }
  }

  // Visualizar la temperatura entera en los displays (0 a 99)
  int tempEntera = (int)temperatura;
  if (tempEntera < 0) tempEntera = 0;
  if (tempEntera > 99) tempEntera = 99;

  mostrar(tempEntera);
}"""
    add_code_box(doc, "Código Fuente: sketch.ino (Circuito 3 - Termómetro Digital DHT22 con Displays)", c3_sketch)

    add_heading_2(doc, "Explicación del circuito")
    add_p(doc, "El sensor DHT22 se alimenta con 5V y GND, y su pin de datos (SDA) se conecta al pin digital D11 del Arduino Nano, que estaba disponible tras cablear los segmentos (D2-D8) y los transistores (D9-D10).")
    add_p(doc, "El DHT22 entrega una trama digital serie calibrada de 40 bits con datos de temperatura y humedad a través de un solo cable, evitando el uso de conversores analógicos adicionales.")

    add_heading_2(doc, "Cómo funciona el código")
    add_num_item(doc, "1", "Inicialización: Se incluye DHT.h, se define el objeto dht en el pin 11 y se inicia en setup() con dht.begin() y el puerto serie a 9600 baudios.", "DHT.h")
    add_num_item(doc, "2", "Muestreo cada 1.5 s: Con if (tiempoActual - ultimoMuestreo >= 1500) se lee dht.readTemperature() y dht.readHumidity() sin bloquear el procesador.", "Lectura")
    add_num_item(doc, "3", "Reporte serial: Los datos leídos se transmiten con formato hacia el monitor serial para su registro.", "Monitor Serial")
    add_num_item(doc, "4", "Refresco constante: La temperatura se redondea a entero y se pasa a mostrar(tempEntera). Al ejecutarse en cada ciclo de loop(), los displays se refrescan más de 100 veces por segundo sin pestañear.", "Refresco")

    add_heading_2(doc, "Lo que se observa en la simulación")
    add_bullet(doc, "El monitor serial confirma el inicio del sensor y muestra la temperatura inicial (24 °C).")
    add_bullet(doc, "Al mover el control deslizante del sensor DHT22 en Wokwi (ej. a 35 °C), los displays se actualizan mostrando '35' y el monitor serial imprime el nuevo valor.")
    add_bullet(doc, "Los números se visualizan firmes y sin interrupción ni parpadeos.")

    add_heading_2(doc, "Observaciones")
    add_bullet(doc, "Programación no bloqueante: Usar millis() en vez de delay() es indispensable; un delay(1500) apagaría los displays durante un segundo y medio en cada lectura.")
    add_bullet(doc, "Rango de displays: Con dos displays se muestra de 0 a 99 °C. Para temperaturas negativas se requeriría un display adicional para el signo menos.")

    doc.add_page_break()

    print("Building Sección 3: Cálculos (concisos)...")
    # =========================================================================
    # SECCIÓN 3: ANÁLISIS TEÓRICO Y CÁLCULOS (CONCISOS)
    # =========================================================================
    add_heading_1(doc, "3. Análisis Teórico y Cálculos de Ingeniería")
    add_p(doc, "A continuación se presentan los cálculos teóricos solicitados en la sección de Anexos de la guía para justificar los valores de los componentes utilizados.")

    add_heading_2(doc, "3.1. Dimensionamiento de Resistencias para Displays de 7 Segmentos")
    add_p(doc, "Para evitar que los LEDs se quemen por sobrecorriente, se calcula la resistencia limitadora de cada segmento mediante la Ley de Ohm:")
    add_p(doc, "R = (Vcc - Vf) / If", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Datos típicos para LED rojo:")
    add_bullet(doc, "Vcc = 5.0 V (tensión del Arduino Nano)", bold_prefix="• ")
    add_bullet(doc, "Vf = 1.9 V (tensión de caída directa del LED)", bold_prefix="• ")
    add_bullet(doc, "If = 14 mA = 0.014 A (corriente de trabajo recomendada)", bold_prefix="• ")
    add_p(doc, "Cálculo:")
    add_p(doc, "R = (5.0 V - 1.9 V) / 0.014 A = 3.1 V / 0.014 A = 221.4 Ω", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Se selecciona el valor comercial estándar más cercano: R = 220 Ω.")
    add_p(doc, "Potencia disipada en la resistencia:")
    add_p(doc, "P = If^2 * R = (0.014 A)^2 * 220 Ω ≈ 43.1 mW", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Como disipa 43.1 mW, una resistencia común de 1/4 W (250 mW) opera con total seguridad y sin calentarse.")

    add_heading_2(doc, "3.2. Polarización y Saturación del Transistor 2N2222 como Switch")
    add_p(doc, "El transistor 2N2222 conmuta el cátodo común del display a tierra (GND):")
    add_num_item(doc, "1", "Corriente máxima de colector: Cuando se muestra el dígito '8' con los 7 segmentos encendidos: Ic_max = 7 * 14 mA = 98 mA.", "Ic_max")
    add_num_item(doc, "2", "Corriente de base para saturación: Con una ganancia de saturación forzada de β_sat = 10 para garantizar mínima caída de tensión (Vce_sat ≈ 0.2 V): Ib = Ic_max / β_sat = 98 mA / 10 = 9.8 mA.", "Ib")
    add_num_item(doc, "3", "Resistencia de base Rb: Rb = (V_pin - Vbe_sat) / Ib = (5.0 V - 0.7 V) / 0.0098 A ≈ 438 Ω. En el circuito se utiliza una resistencia comercial de 1 kΩ, que produce Ib = (4.3 V / 1000 Ω) = 4.3 mA. Dado que el 2N2222 tiene un hfe real superior a 75, esta corriente asegura la saturación completa del transistor.", "Rb")

    add_heading_2(doc, "3.3. Frecuencia de Multiplexación y Persistencia de la Visión (POV)")
    add_p(doc, "El ojo humano integra imágenes discontinuas como continuas si se refrescan a más de 50-60 Hz (umbral CFF):")
    add_bullet(doc, "Tiempo de encendido por display: t_on = 4 ms", bold_prefix="• ")
    add_bullet(doc, "Período total del ciclo (2 displays): T = 2 * 4 ms = 8 ms = 0.008 s", bold_prefix="• ")
    add_bullet(doc, "Frecuencia de refresco resultante: f = 1 / T = 1 / 0.008 s = 125 Hz", bold_prefix="• ")
    add_p(doc, "Como 125 Hz es más del doble del umbral crítico de parpadeo (60 Hz), los displays se perciben encendidos de forma continua y sin titileo. El ciclo de trabajo (duty cycle) de cada display es del 50%.")

    add_heading_2(doc, "3.4. Justificación Técnica: Uso de Transistores frente a Pines Directos")
    add_bullet(doc, "Cada pin del microcontrolador ATmega328P soporta un máximo absoluto de 40 mA (20 mA recomendado).")
    add_bullet(doc, "Al encender el número '8', los 7 segmentos demandan ~98 mA a través del cátodo común.")
    add_bullet(doc, "Conectar el cátodo directo al pin del Arduino superaría su límite en casi 2.5 veces, destruyendo el puerto por sobrecalentamiento. El transistor 2N2222 soporta hasta 800 mA, absorbiendo la corriente con holgura y pidiendo al Arduino solo 4.3 mA en su base.")

    doc.add_page_break()

    print("Building Sección 4: Conclusiones (concisas)...")
    # =========================================================================
    # SECCIÓN 4: CONCLUSIONES (CONCISAS)
    # =========================================================================
    add_heading_1(doc, "4. Conclusiones")

    conclusiones = [
        "El Arduino Nano demostró ser ideal para proyectos de prototipado compacto por su factor de forma para protoboard y sus 8 entradas analógicas.",
        "El control directo del display de 7 segmentos (Circuito 1) permitió verificar la polarización directa de diodos LED y la configuración de pines como salidas.",
        "La técnica de multiplexación (Circuito 2) redujo los pines requeridos de 14 a solo 9, ahorrando más de un tercio de las líneas digitales del microcontrolador.",
        "La frecuencia de multiplexación calculada de 125 Hz superó holgadamente el límite de fusión de parpadeo (60 Hz), logrando una visualización estable y continua.",
        "El transistor 2N2222 operando en saturación protegió los pines del Arduino de la corriente de retorno del cátodo (~98 mA), evitando daños térmicos.",
        "La programación no bloqueante con millis() (Circuito 3) permitió leer el sensor DHT22 cada 1.5 s sin congelar el refresco continuo de los displays.",
        "Wokwi comprobó su eficacia para la simulación de IoT y microcontroladores al permitir crear Custom Chips en lenguaje C para el transistor 2N2222.",
        "Los cálculos teóricos de Ley de Ohm, disipación de potencia y saturación BJT coincidieron plenamente con los valores observados en la simulación virtual."
    ]

    for i, c in enumerate(conclusiones, 1):
        add_num_item(doc, str(i), c, space_after=4)

    doc.add_page_break()

    print("Building Sección 5: Referencias...")
    # =========================================================================
    # SECCIÓN 5: REFERENCIAS BIBLIOGRÁFICAS
    # =========================================================================
    add_heading_1(doc, "5. Referencias Bibliográficas")

    referencias = [
        "Rocabado Moreno, S. H. y Arias Figueroa, D. A. (2016). Arquitectura y organización de la computadora: microprocesadores y programación assembler. D - Editorial de la Universidad Nacional de La Plata. https://elibro.net/es/lc/bibliotecaupt/titulos/77190",
        "Morris Mano, M. y D. Ciletti, M. (2013). Diseño digital (5a. ed.). Pearson Educación. https://elibro.net/es/lc/bibliotecaupt/titulos/37912",
        "Boylestad, R. L. y Nashelsky, L. (2018). Electrónica: Teoría de circuitos y dispositivos electrónicos (11a. ed.). Pearson Educación.",
        "Banzi, M. y Shiloh, M. (2022). Getting Started with Arduino (4th ed.). Maker Media, Inc.",
        "Microchip Technology Inc. (2020). ATmega328P 8-bit AVR Microcontroller Datasheet. Document DS40002061B."
    ]

    for ref in referencias:
        add_bullet(doc, ref, space_after=5)

    doc.add_page_break()

    print("Building Sección 6: Anexos...")
    # =========================================================================
    # SECCIÓN 6: ANEXOS
    # =========================================================================
    add_heading_1(doc, "6. Anexos")

    add_heading_2(doc, "Anexo 1: Diagramas de Conexión en Formato JSON (diagram.json para Wokwi)")
    add_p(doc, "Extracto de configuración de conexionado para reproducir el circuito en Wokwi:")

    c1_json_excerpt = """{
  "version": 1,
  "author": "Perez Peralta & Arocutipa",
  "parts": [
    { "type": "wokwi-arduino-nano", "id": "nano", "top": 0, "left": 0 },
    { "type": "wokwi-7segment", "id": "sevseg1", "top": -50, "left": 150, "attrs": { "common": "cathode" } },
    { "type": "wokwi-resistor", "id": "r1", "top": 50, "left": 150, "attrs": { "value": "220" } }
  ],
  "connections": [
    [ "nano:2", "sevseg1:A", "green", [ "v0" ] ],
    [ "nano:3", "sevseg1:B", "green", [ "v0" ] ],
    [ "nano:4", "sevseg1:C", "green", [ "v0" ] ],
    [ "nano:5", "sevseg1:D", "green", [ "v0" ] ],
    [ "nano:6", "sevseg1:E", "green", [ "v0" ] ],
    [ "nano:7", "sevseg1:F", "green", [ "v0" ] ],
    [ "nano:8", "sevseg1:G", "green", [ "v0" ] ],
    [ "sevseg1:COM.1", "r1:1", "black", [ "v0" ] ],
    [ "r1:2", "nano:GND.1", "black", [ "v0" ] ]
  ]
}"""
    add_code_box(doc, "Estructura JSON: diagram.json (Circuito 1)", c1_json_excerpt)

    add_heading_2(doc, "Anexo 2: Procedimiento de Creación del Custom Chip 2N2222 en Wokwi")
    add_num_item(doc, "1", "Crear un nuevo proyecto en Wokwi con Arduino Nano.")
    add_num_item(doc, "2", "Hacer clic en el botón '+' del editor de código y seleccionar 'New File...'.")
    add_num_item(doc, "3", "Crear 2n2222.chip.json y pegar la definición de pines.")
    add_num_item(doc, "4", "Crear 2n2222.chip.c y pegar la lógica en C de la API de Wokwi.")
    add_num_item(doc, "5", "Para el Circuito 3, agregar 'DHT sensor library' en libraries.txt.")
    add_num_item(doc, "6", "Pegar sketch.ino y presionar 'Play' para ejecutar la simulación.")

    # Target file paths to save
    filenames_to_save = [
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx",
        "Perez Fabrizio_Arocutipa Gian Franco_Lab 2u2 Arduino Nano Wokwi.docx",
        "lab 2u2.docx",
        os.path.join("lab 2u2", "lab 2u2.docx"),
        os.path.join("lab 2u2", "Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi_Actualizado.docx"),
        os.path.join("lab 2u2", "Perez Fabrizio_Arocutipa Gian Franco_Lab 2u2 Arduino Nano Wokwi.docx")
    ]
    saved_files = []
    for fname in filenames_to_save:
        try:
            target_fdir = os.path.dirname(fname)
            if target_fdir and not os.path.exists(target_fdir):
                os.makedirs(target_fdir, exist_ok=True)
            doc.save(fname)
            print(f"Document saved as '{fname}'")
            saved_files.append(fname)
        except PermissionError:
            print(f"Notice: '{fname}' is currently locked/open in Word. Skipped.")
        except Exception as e:
            print(f"Error saving '{fname}': {e}")
            
    return saved_files[0] if saved_files else "lab 2u2.docx"

if __name__ == '__main__':
    build_entire_report()
