import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import io


def extract_text_from_scanned_pdf(pdf_path, output_txt_path):
    """
    Extracts text from a scanned PDF using OCR and saves it to a text file.
    """
    print(f"Converting PDF '{pdf_path}' to images...")
    pages = convert_from_path(pdf_path, dpi=300)

    extracted_text = []

    print("Performing OCR on each page...")
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        extracted_text.append(f"— — PAGE {i+1} — —\n")
        extracted_text.append(text)

    full_text = "".join(extracted_text)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Text extraction complete. Output saved to '{output_txt_path}'")
    return full_text


def ocr_pdf_directory(input_dir, output_dir="fixed_pdf"):
    """
    OCR all PDFs in a directory and store text files in fixed_pdf.
    Only performs OCR if the corresponding .txt does NOT already exist.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            txt_name = os.path.splitext(file)[0] + ".txt"
            txt_path = os.path.join(output_dir, txt_name)

            # 🔥 NEW: Skip if already OCR-ed
            if os.path.exists(txt_path):
                print(f"⏭ Skipping OCR (already exists): {txt_path}")
                continue

            extract_text_from_scanned_pdf(pdf_path, txt_path)


# =======================
# Example Usage
# =======================
if __name__ == "__main__":
    pdf_dir = r"F:\RAG pipeline\data"
    ocr_pdf_directory(pdf_dir)
    print("All done!")