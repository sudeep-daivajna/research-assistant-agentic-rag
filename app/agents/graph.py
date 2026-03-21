from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.agents.retriever import retriever_node
from app.agents.analyser import analyser_node
from app.agents.synthesizer import synthesizer_node

class AgentState(TypedDict):
    question: str
    user_id: int
    retrieved_chunks: List[str]
    analysis: str
    final_answer: str

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retriever", retriever_node)
    graph.add_node("analyser", analyser_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.set_entry_point("retriever")
    graph.add_edge("retriever", "analyser")
    graph.add_edge("analyser", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()

research_graph = build_graph()