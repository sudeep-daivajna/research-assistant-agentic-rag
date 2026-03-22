from app.agents.retriever import retriever_node
from app.agents.analyser import analyser_node
from app.agents.synthesizer import synthesizer_node
from app.db.mongo import get_mongo_db
import datetime
import time

AGENTS = {
    "retriever": retriever_node,
    "analyser": analyser_node,
    "synthesizer": synthesizer_node
}

async def run_session(db, user_id: int, session_id: int, question: str):
    mongo = get_mongo_db()

    state = {
        "question": question,
        "user_id": user_id,
        "retrieved_chunks": [],
        "analysis": "",
        "final_answer": ""
    }

    for agent_name, agent_fn in AGENTS.items():
        start = time.time()
        try:
            state = await agent_fn(state)
            duration = int((time.time() - start) * 1000)
            await db.execute(
                """INSERT INTO execution_logs 
                   (session_id, agent_name, status, duration_ms)
                   VALUES ($1, $2, $3, $4)""",
                session_id, agent_name, "success", duration
            )
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            await db.execute(
                """INSERT INTO execution_logs 
                   (session_id, agent_name, status, duration_ms)
                   VALUES ($1, $2, $3, $4)""",
                session_id, agent_name, "failed", duration
            )
            await db.execute(
                "UPDATE sessions SET status='failed' WHERE id=$1", session_id
            )
            print(f"Agent {agent_name} failed: {e}")
            return

    await mongo["agent_outputs"].insert_one({
        "session_id": session_id,
        "user_id": user_id,
        "question": question,
        "retrieved_chunks": state["retrieved_chunks"],
        "analysis": state["analysis"],
        "final_answer": state["final_answer"],
        "created_at": datetime.datetime.utcnow()
    })

    await db.execute(
        "UPDATE sessions SET status='completed', completed_at=$1 WHERE id=$2",
        datetime.datetime.utcnow(), session_id
    )