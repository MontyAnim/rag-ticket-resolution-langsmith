import logging
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.load import loads
from cachetools import TTLCache, cached
from src.core.config import settings

logger = logging.getLogger(__name__)

# Fallback prompt in case the Hub is unreachable or the prompt handle is invalid
FALLBACK_SYSTEM_PROMPT = (
    "You are a helpful and precise technical support resolution assistant. "
    "Use the `retrieve_knowledge` tool to look up technical documentation and troubleshooting manuals. "
    "Use the `query_ticket_status` tool to check previous ticket history and details in the database. "
    "Always be polite, concise, and provide accurate answers based on the retrieved context."
)

prompt_cache = TTLCache(maxsize=10, ttl=300)

@cached(cache=prompt_cache)
def get_react_prompt() -> ChatPromptTemplate:
    """
    Dynamically pulls the prompt template from LangSmith Hub.
    Falls back to a hardcoded template if the pull fails.
    """
    prompt_handle = settings.LANGCHAIN_HUB_PROMPT
    
    try:
        # Client().pull_prompt returns a ChatPromptTemplate
        logger.info(f"Attempting to pull prompt from LangChain Hub: {prompt_handle}")
        client = Client()
        prompt = client.pull_prompt(prompt_handle)
        if isinstance(prompt, str):
            prompt = loads(prompt)
        return prompt
    except Exception as e:
        logger.warning(f"Failed to pull prompt '{prompt_handle}' from Hub: {e}. Using fallback prompt.")
        return ChatPromptTemplate.from_messages([
            ("system", FALLBACK_SYSTEM_PROMPT),
            ("placeholder", "{messages}")
        ])
