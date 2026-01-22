from pathlib import Path
from src.pdf_checker import prepare_unified_fixed_folder
from src.data_loader import load_all_documents
from src.pdf_to_text import ocr_pdf_directory
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

if __name__ == "__main__":
    """
    SOURCE_DATA_DIR = "data"
    FIXED_DIR = Path(SOURCE_DATA_DIR) / "fixed_pdfs"

    # 1️⃣ Check if fixed_pdfs already has PDFs
    existing_fixed_pdfs = set()
    if FIXED_DIR.exists():
        existing_fixed_pdfs = {
            p.name for p in FIXED_DIR.glob("*.pdf")
        }

    # 2️⃣ Check raw PDFs
    raw_pdfs = {
        p.name for p in Path(SOURCE_DATA_DIR).glob("*.pdf")
    }

    # 3️⃣ Decide whether OCR is needed
    pdfs_to_ocr = raw_pdfs - existing_fixed_pdfs

    if pdfs_to_ocr:
        print(f"[INFO] OCR required for {len(pdfs_to_ocr)} new PDFs")
        ocr_pdf_directory(SOURCE_DATA_DIR)
    else:
        print("[INFO] All PDFs already OCR-processed. Skipping OCR.")

    # 4️⃣ Prepare unified fixed folder (safe to call)
    fixed_folder, fixed_files = prepare_unified_fixed_folder(SOURCE_DATA_DIR)

    print("OCR and cleaning completed")
    print(f"Using fixed PDFs from: {fixed_folder}")
    print(f"Total PDFs ready: {len(fixed_files)}")"""

    # 5️⃣ Load documents ONLY from fixed folder
    docs = load_all_documents("fixed_pdf")
    print(f"Loaded {len(docs)} multimodal documents")

    # 6️⃣ Build vector store
    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)
    store.load()

    rag_search = RAGSearch()

    while True:
        query = input("what is your query : ")
        if query.lower() == "exit":
            break

        summary = rag_search.search_and_summarize(
            query=query,
            top_k=6
        )
        print("\nSummary:", summary)
