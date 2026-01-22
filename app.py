from src.pdf_checker import prepare_unified_fixed_folder
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch
from src.embedding import EmbeddingPipeline
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader


if __name__ == "__main__":

    SOURCE_DATA_DIR = "data"

    fixed_folder, fixed_files = prepare_unified_fixed_folder(SOURCE_DATA_DIR)

    print(f"OCR and cleaning completed")
    print(f"Using fixed PDFs from: {fixed_folder}")
    print(f"Total PDFs ready: {len(fixed_files)}")

    docs = load_all_documents(fixed_folder)
    print(f"Loaded {len(docs)} documents")

  
    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)
    store.load()

    rag_search = RAGSearch()

    while True:
        query = input("what is your query : ")
        if query.lower() == "exit":
            break

        summary = rag_search.search_and_summarize(query=query, top_k=6)
        print("Summary:", summary)
