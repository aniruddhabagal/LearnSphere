# vectorstore.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import pickle

VECTORSTORE_PATH = 'vectorstore/faiss_index.pkl'

def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = FAISS.from_documents(docs, embeddings)
    os.makedirs('vectorstore', exist_ok=True)
    with open(VECTORSTORE_PATH, 'wb') as f:
        pickle.dump(vectorstore, f)
    return vectorstore

def load_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        with open(VECTORSTORE_PATH, 'rb') as f:
            vectorstore = pickle.load(f)
        return vectorstore
    else:
        return None
