import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager")
    sync_database_url: str = os.getenv("SYNC_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/task_manager")
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-jwt-key-change-in-production-1234567890")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
