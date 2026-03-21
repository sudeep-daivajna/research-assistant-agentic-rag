from app.db.postgres import get_pool

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          SERIAL PRIMARY KEY,
                email       VARCHAR(255) UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                created_at  TIMESTAMP DEFAULT NOW()
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id           SERIAL PRIMARY KEY,
                user_id      INTEGER REFERENCES users(id),
                question     TEXT NOT NULL,
                status       VARCHAR(50) DEFAULT 'pending',
                created_at   TIMESTAMP DEFAULT NOW(),
                completed_at TIMESTAMP
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS execution_logs (
                id           SERIAL PRIMARY KEY,
                session_id   INTEGER REFERENCES sessions(id),
                agent_name   VARCHAR(100),
                status       VARCHAR(50),
                duration_ms  INTEGER,
                created_at   TIMESTAMP DEFAULT NOW()
            );
        """)