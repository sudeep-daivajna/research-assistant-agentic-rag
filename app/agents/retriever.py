from app.db.vector import get_vector_store
from app.db.mongo import get_mongo_db
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

async def retriever_node(state: dict) -> dict:
    question = state["question"]
    user_id = state["user_id"]

    question_embedding = model.encode([question])
    vector_store = get_vector_store()

    distances, indices = vector_store.search(
        np.array(question_embedding).astype("float32"), k=5
    )

    faiss_ids = [int(i) for i in indices[0] if i != -1]

    db = get_mongo_db()
    chunks = await db["chunk_index"].find(
        {"faiss_id": {"$in": faiss_ids}, "user_id": user_id}
    ).to_list(length=10)

    retrieved = [c["chunk"] for c in chunks]

    return {**state, "retrieved_chunks": retrieved}