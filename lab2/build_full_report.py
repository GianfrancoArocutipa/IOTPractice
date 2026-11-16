# -*- coding: utf-8 -*-
"""
Script to generate the complete, perfectly formatted Lab 2.2 Word document report:
'Perez Fabrizio_Arocutipa Gian Franco_Lab 2.2 Arduino Nano Wokwi.docx'
Matching the exact layout, color palette, typography, headers, footers, structure,
code boxes, and screenshot placeholders from Lab 2.1 report.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
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

def add_header_footer(doc):
    """Configures header and footer matching the exact style of the reference report."""
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True

    # HEADER (Pages 2+)
    header = section.header
    header_tbl = header.add_table(rows=1, cols=2, width=Inches(6.25))
    header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Left cell: UPT Logo
    cell_l = header_tbl.rows[0].cells[0]
    cell_l.width = Inches(0.8)
    set_cell_borders(cell_l, bottom="single", color="000000", sz="6")
    set_cell_margins(cell_l, top=0, bottom=80, left=0, right=0)
    p_img = cell_l.paragraphs[0]
    p_img.paragraph_format.space_before = Pt(0)
    p_img.paragraph_format.space_after = Pt(2)
    header_logo_path = os.path.abspath('extracted_assets/header_logo_18.png')
    if os.path.exists(header_logo_path):
        p_img.add_run().add_picture(header_logo_path, width=Inches(0.35))
    
    # Right cell: Institution name
    cell_r = header_tbl.rows[0].cells[1]
    cell_r.width = Inches(5.45)
    set_cell_borders(cell_r, bottom="single", color="000000", sz="6")
    set_cell_margins(cell_r, top=0, bottom=80, left=0, right=0)
    p_txt = cell_r.paragraphs[0]
    p_txt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_txt.paragraph_format.space_before = Pt(6)
    p_txt.paragraph_format.space_after = Pt(2)
    r = p_txt.add_run('Escuela Profesional de Ingeniería de Sistemas')
    r.font.name = 'Arial'
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0, 0, 0)

    # FOOTER (Pages 2+)
    footer = section.footer
    footer_tbl = footer.add_table(rows=1, cols=2, width=Inches(6.25))
    footer_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Left cell: Page number
    f_cell_l = footer_tbl.rows[0].cells[0]
    f_cell_l.width = Inches(2.5)
    set_cell_borders(f_cell_l, top="single", color="000000", sz="6")
    set_cell_margins(f_cell_l, top=80, bottom=0, left=0, right=0)
    p_pg = f_cell_l.paragraphs[0]
    p_pg.paragraph_format.space_before = Pt(4)
    p_pg.paragraph_format.space_after = Pt(0)
    p_pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    r_dash1 = p_pg.add_run('- ')
    r_dash1.font.name = 'Arial'
    r_dash1.font.size = Pt(10)
    r_dash1.font.color.rgb = RGBColor(0, 0, 0)

    # XML PAGE FIELD
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p_pg._p.append(fldSimple)

    r_dash2 = p_pg.add_run(' -')
    r_dash2.font.name = 'Arial'
    r_dash2.font.size = Pt(10)
    r_dash2.font.color.rgb = RGBColor(0, 0, 0)

    # Right cell: Teacher name
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

print("Helper functions defined.")
