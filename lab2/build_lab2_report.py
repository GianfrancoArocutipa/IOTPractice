# -*- coding: utf-8 -*-
"""
Generator for:
'Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi.docx'
Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas
Curso: Internet de las Cosas
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="000000", sz="4"):
    """Sets borders of a table cell."""
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
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
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
    """Sets Letter size, standard margins and different first page."""
    for s in doc.sections:
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.0)
        s.different_first_page_header_footer = True

        # Setup Header (Pages 2+)
        header = s.header
        header_tbl = header.add_table(rows=1, cols=2, width=Inches(6.25))
        header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Left header cell: Logo
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
        
        # Right header cell: Text
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

        # Setup Footer (Pages 2+)
        footer = s.footer
        footer_tbl = footer.add_table(rows=1, cols=2, width=Inches(6.25))
        footer_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Left footer cell: Page number
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

        # Right footer cell: Teacher name
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

def add_p(doc, text="", style='Normal', space_before=0, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, font_size=11, color_rgb=(0,0,0)):
    """Helper to add standard body paragraph."""
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

def add_bullet(doc, text, bold_prefix="", space_after=4):
    """Helper to add bullet item."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    # Bullet symbol
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

def add_heading_1(doc, text, space_before=14, space_after=6):
    """Major heading 1."""
    return add_p(doc, text, bold=True, font_size=11, space_before=space_before, space_after=space_after)

def add_heading_2(doc, text, space_before=10, space_after=4):
    """Subheading 2."""
    return add_p(doc, text, bold=True, font_size=11, space_before=space_before, space_after=space_after)

def add_wokwi_link(doc, url):
    """Adds a highlighted Wokwi project link."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
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
    """Renders a code snippet inside a light gray shaded container with Consolas font."""
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(3)
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
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    p_code = cell.paragraphs[0]
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.0

    r_code = p_code.add_run(code_content.strip())
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(9)
    r_code.font.color.rgb = RGBColor(0, 0, 0)

    # Empty paragraph after table for spacing
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_capture_placeholder(doc, capture_num, title, instructions_list):
    """
    Renders an elegant, prominent placeholder box where the student must paste their screenshot.
    Clearly specifies what elements must be captured and the required simulation state.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.25)
    set_cell_background(cell, "F4F6F9")
    set_cell_borders(cell, top="dashed", bottom="dashed", left="dashed", right="dashed", color="2E5B82", sz="12")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    # Box title
    p_h = cell.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(2)
    p_h.paragraph_format.space_after = Pt(4)
    r_icon = p_h.add_run("📷 ESPACIO PARA CAPTURA DE PANTALLA Nº " + str(capture_num) + "\n")
    r_icon.font.name = 'Arial'
    r_icon.font.bold = True
    r_icon.font.size = Pt(11)
    r_icon.font.color.rgb = RGBColor(46, 91, 130)

    r_title = p_h.add_run(title.upper())
    r_title.font.name = 'Arial'
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    # Divider line
    p_div = cell.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(4)
    r_div = p_div.add_run("─" * 58)
    r_div.font.name = 'Arial'
    r_div.font.size = Pt(8)
    r_div.font.color.rgb = RGBColor(180, 190, 200)

    # Instructions header
    p_inst = cell.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(2)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst_h = p_inst.add_run("¿Qué debe mostrar esta captura?:")
    r_inst_h.font.name = 'Arial'
    r_inst_h.font.bold = True
    r_inst_h.font.size = Pt(9.5)
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
        rb_sym.font.size = Pt(9)
        rb_sym.font.color.rgb = RGBColor(0, 128, 0)

        rb_txt = p_b.add_run(item)
        rb_txt.font.name = 'Arial'
        rb_txt.font.size = Pt(9)
        rb_txt.font.color.rgb = RGBColor(40, 40, 40)

    # Blank paste prompt
    p_paste = cell.add_paragraph()
    p_paste.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_paste.paragraph_format.space_before = Pt(14)
    p_paste.paragraph_format.space_after = Pt(14)
    r_paste = p_paste.add_run("[ HAGA CLIC AQUÍ Y PEGUE (Ctrl+V) SU CAPTURA DE PANTALLA ]")
    r_paste.font.name = 'Arial'
    r_paste.font.italic = True
    r_paste.font.bold = True
    r_paste.font.size = Pt(9.5)
    r_paste.font.color.rgb = RGBColor(120, 130, 140)

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(0)
    p_post.paragraph_format.space_after = Pt(6)

def add_guide_image(doc, img_path, caption, width_in=5.8):
    """Inserts a diagram image from the teacher's guide with caption."""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.add_run().add_picture(img_path, width=Inches(width_in))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(80, 80, 80)

print("Base layout and component functions ready.")
