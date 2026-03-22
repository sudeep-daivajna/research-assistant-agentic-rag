from app.db.mongo import get_mongo_db
from app.db.vector import get_vector_store, save_vector_store
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

async def ingest_document(user_id: int, title: str, content: str) -> dict:
    chunks = chunk_text(content)
    embeddings = model.encode(chunks)

    db = get_mongo_db()

    doc = {
        "user_id": user_id,
        "title": title,
        "chunks": chunks,
        "created_at": __import__("datetime").datetime.utcnow()
    }
    result = await db["documents"].insert_one(doc)
    doc_id = str(result.inserted_id)

    vector_store = get_vector_store()
    ids = list(range(vector_store.ntotal, vector_store.ntotal + len(chunks)))
    
    await db["chunk_index"].insert_many([
        {"faiss_id": ids[i], "doc_id": doc_id, "user_id": user_id, "chunk": chunks[i]}
        for i in range(len(chunks))
    ])

    vector_store.add(np.array(embeddings).astype("float32"))
    save_vector_store()

    return {"doc_id": doc_id, "chunks_stored": len(chunks)}