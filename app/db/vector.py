import faiss
import os

_vector_store = None
EMBEDDING_DIM = 384
FAISS_PATH = "faiss_index.bin"

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        if os.path.exists(FAISS_PATH):
            _vector_store = faiss.read_index(FAISS_PATH)
        else:
            _vector_store = faiss.IndexFlatL2(EMBEDDING_DIM)
    return _vector_store

def save_vector_store():
    if _vector_store is not None:
        faiss.write_index(_vector_store, FAISS_PATH)