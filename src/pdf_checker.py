import fitz
import re
import os
import shutil
import pytesseract
from pdf2image import convert_from_path

def is_gibberish(text):
    clean_text = re.sub(r'[^a-zA-Z]', '', text)
    if len(clean_text) < 10: return False
    vowels = sum(1 for c in clean_text.lower() if c in 'aeiou')
    return (vowels / len(clean_text)) < 0.15

def run_ocr_fix_windows(input_path, output_path):
    print(f"  ⚙️ [OCR] Processing: {os.path.basename(input_path)}")
    try:
        pages = convert_from_path(input_path, dpi=300)
        result_pdf = fitz.open()
        for page_image in pages:
            page_pdf_bytes = pytesseract.image_to_pdf_or_hocr(page_image, extension='pdf')
            with fitz.open("pdf", page_pdf_bytes) as page_pdf:
                result_pdf.insert_pdf(page_pdf)
        result_pdf.save(output_path)
        result_pdf.close()
        return True
    except Exception as e:
        print(f"  ❌ OCR Failed for {input_path}: {e}")
        return False

def prepare_unified_fixed_folder(source_dir):
    # 1. Setup the target folder
    fixed_dir = os.path.join(source_dir, "fixed_pdfs")
    if not os.path.exists(fixed_dir):
        os.makedirs(fixed_dir)
        print(f"📁 Created unified folder: {fixed_dir}")

    final_paths = []

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(source_dir, filename)
            output_path = os.path.join(fixed_dir, filename) # Keep original name

            # 2. Check if file is already in 'fixed_pdfs'
            if os.path.exists(output_path):
                final_paths.append(output_path)
                continue

            # 3. Decision Logic
            doc = fitz.open(file_path)
            needs_ocr = False
            for page in doc.pages(0, min(len(doc), 2)):
                text = page.get_text()
                if not text.strip() or is_gibberish(text):
                    needs_ocr = True ; break
            doc.close()

            if needs_ocr:
                # OPTION A: Fix and Save to 'fixed_pdfs'
                if run_ocr_fix_windows(file_path, output_path):
                    final_paths.append(output_path)
            else:
                # OPTION B: Clean - Copy as-is to 'fixed_pdfs'
                print(f"  ✅ [Clean] Copying to fixed folder: {filename}")
                shutil.copy2(file_path, output_path)
                final_paths.append(output_path)

    return fixed_dir, final_paths,
