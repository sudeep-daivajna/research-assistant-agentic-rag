import asyncpg
from app.config import settings

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            settings.POSTGRES_URL.replace("postgresql+asyncpg://", "postgresql://")
        )
    return _pool

async def get_db():
    pool = await get_pool()
    async with pool.acquire() as connection:
        yield connection