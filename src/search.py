import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
load_dotenv()


class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "llama-3.3-70b-versatile"
    ):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)

        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from src.data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=llm_model
        )

        self.chat_history = []
    
    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r.get("metadata")]

        context = "\n\n".join(texts)

        if not context:
            return "No relevant documents found."

        messages = self.chat_history + [
            HumanMessage(
                content=f"""
Use the context below to answer the query.

Context:
{context}

Query:
{query}
"""
            )
        ]

        response = self.llm.invoke(messages)

        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=response.content))

        return response.content