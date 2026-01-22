import streamlit as st
from dotenv import load_dotenv
from src.pdf_checker import prepare_unified_fixed_folder
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

load_dotenv()

st.set_page_config(page_title="RAG PDF Search", layout="wide")
st.title("RAG PDF Search")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

SOURCE_DATA_DIR = "data"

@st.cache_resource
def setup_pipeline():
    fixed_folder, fixed_files = prepare_unified_fixed_folder(SOURCE_DATA_DIR)
    docs = load_all_documents(fixed_folder)

    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)
    store.load()

    rag_search = RAGSearch()
    return fixed_folder, fixed_files, docs, rag_search


with st.spinner("Preparing system"):
    fixed_folder, fixed_files, docs, rag_search = setup_pipeline()

st.write("Fixed folder:", fixed_folder)
st.write("PDFs:", len(fixed_files))
st.write("Documents:", len(docs))

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

query = st.chat_input("Ask a question")

if query:
    st.session_state.chat_history.append(("user", query))
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Searching"):
        answer = rag_search.search_and_summarize(query=query, top_k=3)

    st.session_state.chat_history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.write(answer)
