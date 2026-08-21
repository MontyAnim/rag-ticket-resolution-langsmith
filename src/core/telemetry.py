import logging
from langsmith import Client
from src.core.config import settings

logger = logging.getLogger(__name__)

# Global LangSmith client instance
ls_client: Client | None = None

def setup_telemetry():
    """
    Initializes the LangSmith client and verifies the telemetry configuration.
    It expects LANGCHAIN_TRACING_V2 to be set in the environment or config.
    """
    global ls_client
    
    if settings.LANGCHAIN_TRACING_V2.lower() == "true":
        if not settings.LANGCHAIN_API_KEY:
            logger.warning("LANGCHAIN_TRACING_V2 is true, but LANGCHAIN_API_KEY is not set. Tracing will fail.")
        else:
            try:
                # Initialize the client. It automatically picks up the API key and Project from env/config
                ls_client = Client(
                    api_key=settings.LANGCHAIN_API_KEY
                )
                logger.info(f"LangSmith telemetry initialized for project: {settings.LANGCHAIN_PROJECT}")
            except Exception as e:
                logger.error(f"Failed to initialize LangSmith telemetry: {e}")
    else:
        logger.info("LangSmith telemetry is disabled (LANGCHAIN_TRACING_V2 != true).")

def get_ls_client() -> Client | None:
    """Returns the global LangSmith client if initialized."""
    return ls_client
