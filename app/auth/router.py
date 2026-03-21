from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.auth.service import register_user, login_user
from app.db.postgres import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(body: RegisterRequest, db=Depends(get_db)):
    user = await register_user(db, body.email, body.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created", "user": user}

@router.post("/login")
async def login(body: LoginRequest, db=Depends(get_db)):
    result = await login_user(db, body.email, body.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result