from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.utils import decode_access_token
from app.db.postgres import get_db

bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db.fetchrow(
        "SELECT id, email FROM users WHERE id = $1", payload["user_id"]
    )

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return dict(user)