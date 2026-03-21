import faiss

_vector_store = None
EMBEDDING_DIM = 384

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = faiss.IndexFlatL2(EMBEDDING_DIM)
    return _vector_store