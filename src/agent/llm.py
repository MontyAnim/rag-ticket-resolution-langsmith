from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_llm(temperature: float = 0.0):
    """
    Factory function to initialize the LLM based on available API keys.
    Prioritizes Groq if available (for free/fast local testing), 
    otherwise falls back to OpenAI.
    """
    if settings.GROQ_API_KEY:
        logger.info("Initializing Groq LLM (openai/gpt-oss-120b)")
        return ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=settings.GROQ_API_KEY,
            temperature=temperature
        )
    elif settings.OPENAI_API_KEY:
        logger.info("Initializing OpenAI LLM (gpt-4o-mini)")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature
        )
    else:
        raise ValueError("No LLM API keys found. Please set GROQ_API_KEY or OPENAI_API_KEY in your .env file.")
