from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

def create_vectorstore(texts):
    embeddings = OllamaEmbeddings(model="llama3")
    return FAISS.from_texts(texts, embeddings)