from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.dependencies import get_current_user
from app.documents.service import ingest_document

router = APIRouter(prefix="/documents", tags=["documents"])

class DocumentRequest(BaseModel):
    title: str
    content: str

@router.post("/")
async def upload_document(
    body: DocumentRequest,
    current_user = Depends(get_current_user)
):
    result = await ingest_document(current_user["id"], body.title, body.content)
    return {"message": "Document ingested", **result}