from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client = None

def get_mongo_db():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)
    
    return _client[settings.MONGO_DB_NAME] #which specific database inside that servers