from langchain_groq import ChatGroq
from app.config import settings

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama3-8b-8192")

async def analyser_node(state: dict) -> dict:
    question = state["question"]
    chunks = state["retrieved_chunks"]

    if not chunks:
        return {**state, "analysis": "No relevant context found."}

    context = "\n\n".join(chunks)

    prompt = f"""You are a research analyst. Given the question and context below,
identify and extract only the parts of the context that are directly relevant to answering the question.
Be concise.

Question: {question}

Context:
{context}

Relevant information:"""

    response = await llm.ainvoke(prompt)
    return {**state, "analysis": response.content}