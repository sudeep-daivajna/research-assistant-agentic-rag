from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_URL: str

    MONGO_URL: str
    MONGO_DB_NAME: str

    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()