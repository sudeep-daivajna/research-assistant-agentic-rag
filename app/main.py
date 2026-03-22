from fastapi import FastAPI
from app.db.init_db import init_db
from app.auth.router import router as auth_router
from app.documents.router import router as documents_router
from app.sessions.router import router as sessions_router

app = FastAPI(title="Research Assistant", version="1.0.0")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(sessions_router)

@app.get("/health")
async def health():
    return {"status": "ok"}