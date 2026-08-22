from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from dotenv import load_dotenv

# Load .env into os.environ so LangChain's internal tracer can pick it up
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    
    # CORS config
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database config
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag_ops"
    
    # Vector DB config
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    
    # LLMs
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    LLM_PROVIDER: str = "openai"
    LLM_MODEL_NAME: str = "gpt-4o-mini"
    # LangSmith Observability
    LANGSMITH_TRACING: str = "false"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "Rag-Ops Support Engine"
    LANGCHAIN_PROJECT: str = "Rag-Ops Support Engine"
    LANGCHAIN_HUB_PROMPT: str = "support-agent-prompt"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
