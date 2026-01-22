from src.dynamic_multimodal_ocr_rag import extract_multimodal_documents

import os

def load_all_documents(data_dir: str):
    """
    Loads PDFs and returns LangChain Documents
    (text + table rows + figures)
    """
    all_docs = []

    for file in os.listdir(data_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(data_dir, file)
            print(f"[INFO] Processing PDF: {file}")

            docs = extract_multimodal_documents(pdf_path)
            all_docs.extend(docs)

    return all_docs
