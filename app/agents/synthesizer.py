from langchain_groq import ChatGroq
from app.config import settings

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.3-70b-versatile")

async def synthesizer_node(state: dict) -> dict:
    question = state["question"]
    analysis = state["analysis"]

    if analysis == "No relevant context found.":
        return {**state, "final_answer": "I could not find relevant information in your documents to answer this question."}

    prompt = f"""You are a research assistant. Using the analysis below, write a clear and complete answer to the question.
Only use information from the analysis. Do not add outside knowledge.

Question: {question}

Analysis:
{analysis}

Answer:"""

    response = await llm.ainvoke(prompt)
    return {**state, "final_answer": response.content}