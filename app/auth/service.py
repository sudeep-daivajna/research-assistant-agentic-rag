from app.auth.utils import hash_password, verify_password, create_access_token

async def register_user(db, email: str, password: str):
    existing = await db.fetchrow(
        "SELECT id FROM users WHERE email = $1", email
    )
    if existing:
        return None

    hashed = hash_password(password)
    user = await db.fetchrow(
        "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id, email",
        email, hashed
    )
    return dict(user)

async def login_user(db, email: str, password: str):
    user = await db.fetchrow(
        "SELECT id, email, password FROM users WHERE email = $1", email
    )
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None

    token = create_access_token({"user_id": user["id"], "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}