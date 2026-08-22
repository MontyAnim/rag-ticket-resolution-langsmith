import logging
from langsmith import Client
from src.core.config import settings

logger = logging.getLogger(__name__)

# Global LangSmith client instance
ls_client: Client | None = None

def setup_telemetry():
    """
    Initializes the LangSmith client and verifies the telemetry configuration.
    It expects LANGSMITH_TRACING to be set in the environment or config.
    """
    global ls_client
    
    if settings.LANGSMITH_TRACING.lower() == "true":
        if not settings.LANGSMITH_API_KEY:
            logger.warning("LANGSMITH_TRACING is true, but LANGSMITH_API_KEY is not set. Tracing will fail.")
        else:
            try:
                # Initialize the client. It automatically picks up the API key and Project from env/config
                ls_client = Client(
                    api_key=settings.LANGSMITH_API_KEY
                )
                logger.info(f"LangSmith telemetry initialized for project: {settings.LANGSMITH_PROJECT}")
            except Exception as e:
                logger.error(f"Failed to initialize LangSmith telemetry: {e}")
    else:
        logger.info("LangSmith telemetry is disabled (LANGSMITH_TRACING != true).")

def get_ls_client() -> Client | None:
    """Returns the global LangSmith client if initialized."""
    return ls_client
