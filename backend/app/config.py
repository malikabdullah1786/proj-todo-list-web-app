import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager"
    sync_database_url: str = "postgresql://postgres:postgres@localhost:5432/task_manager"
    secret_key: str = "super-secret-jwt-key-change-in-production-1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
