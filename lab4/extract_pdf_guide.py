# -*- coding: utf-8 -*-
"""
Script utilitario para Laboratorio 4:
Extrae texto completo e imagenes de cualquier guia en PDF que se coloque en esta carpeta.
"""

import os
import sys
import glob
import fitz  # PyMuPDF

def extract_pdf_assets(pdf_path=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not pdf_path:
        pdf_files = glob.glob(os.path.join(current_dir, "*.pdf"))
        if not pdf_files:
            print("[AVISO] No se encontro ningun archivo PDF en:", current_dir)
            print("Por favor, sube la guia del Lab 4 en PDF aqui y vuelve a ejecutar.")
            return
        pdf_path = pdf_files[0]

    print(f"[*] Procesando guia: {os.path.basename(pdf_path)}")
    doc = fitz.open(pdf_path)
    
    # 1. Extraer texto completo
    extracted_text_path = os.path.join(current_dir, "lab4_pdf_extracted_text.txt")
    full_text = []
    
    # 2. Carpeta para imagenes
    images_dir = os.path.join(current_dir, "extracted_images")
    os.makedirs(images_dir, exist_ok=True)
    
    img_counter = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text.append(f"--- PAGINA {page_num + 1} ---\n" + text)
        
        # Extraer imagenes
        image_list = page.get_images(full=True)
        for img_idx, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            img_filename = f"page_{page_num + 1}_img_{img_idx + 1}_{img_info[7]}.{image_ext}"
            img_path = os.path.join(images_dir, img_filename)
            with open(img_path, "wb") as f_img:
                f_img.write(image_bytes)
            img_counter += 1

    with open(extracted_text_path, "w", encoding="utf-8") as f_txt:
        f_txt.write("\n\n".join(full_text))

    print(f"[OK] Texto extraido guardado en: {extracted_text_path}")
    print(f"[OK] Se extrajeron {img_counter} imagenes en: {images_dir}")

if __name__ == "__main__":
    pdf_arg = sys.argv[1] if len(sys.argv) > 1 else None
    extract_pdf_assets(pdf_arg)
