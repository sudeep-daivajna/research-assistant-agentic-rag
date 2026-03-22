from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.dependencies import get_current_user
from app.db.postgres import get_db
from app.db.mongo import get_mongo_db
from app.sessions.service import run_session

router = APIRouter(prefix="/sessions", tags=["sessions"])

class SessionRequest(BaseModel):
    question: str

@router.post("/")
async def create_session(
    body: SessionRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    row = await db.fetchrow(
        """INSERT INTO sessions (user_id, question, status)
           VALUES ($1, $2, 'running') RETURNING id""",
        current_user["id"], body.question
    )
    session_id = row["id"]

    await run_session(db, current_user["id"], session_id, body.question)

    session = await db.fetchrow(
        "SELECT status FROM sessions WHERE id=$1", session_id
    )
    return {"session_id": session_id, "status": session["status"]}

@router.get("/{session_id}/results")
async def get_results(
    session_id: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    session = await db.fetchrow(
        "SELECT * FROM sessions WHERE id=$1 AND user_id=$2",
        session_id, current_user["id"]
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    mongo = get_mongo_db()
    output = await mongo["agent_outputs"].find_one({"session_id": session_id})

    if not output:
        raise HTTPException(status_code=404, detail="Results not ready")

    return {
        "question": output["question"],
        "final_answer": output["final_answer"],
        "sources": output["retrieved_chunks"]
    }

@router.get("/{session_id}/logs")
async def get_logs(
    session_id: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    session = await db.fetchrow(
        "SELECT id FROM sessions WHERE id=$1 AND user_id=$2",
        session_id, current_user["id"]
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    logs = await db.fetch(
        "SELECT agent_name, status, duration_ms, created_at FROM execution_logs WHERE session_id=$1",
        session_id
    )
    return {"session_id": session_id, "logs": [dict(l) for l in logs]}