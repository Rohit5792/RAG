from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch
from src.embedding import EmbeddingPipeline

# Example usage
if __name__ == "__main__":
    
    #docs = load_all_documents("data")
    #print(docs)
    store=FaissVectorStore("faiss_store")
    #store.build_from_documents(docs)
    store.load()
    
    rag_search=RAGSearch()
    query=str(input("what is your query :"))
    summary=rag_search.search_and_summarize(query=query,top_k=3)
    print("Summary:",summary)
    