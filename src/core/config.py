from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS config
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database config
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag_ops"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
