import logging
from langchainhub import Client
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from src.core.config import settings

logger = logging.getLogger(__name__)

# Fallback prompt in case the Hub is unreachable or the prompt handle is invalid
FALLBACK_SYSTEM_PROMPT = (
    "You are a helpful and precise technical support resolution assistant. "
    "Use the `retrieve_knowledge` tool to look up technical documentation and troubleshooting manuals. "
    "Use the `query_ticket_status` tool to check previous ticket history and details in the database. "
    "Always be polite, concise, and provide accurate answers based on the retrieved context."
)

def get_react_prompt() -> ChatPromptTemplate:
    """
    Dynamically pulls the prompt template from LangSmith Hub.
    Falls back to a hardcoded template if the pull fails.
    """
    prompt_handle = settings.LANGCHAIN_HUB_PROMPT
    
    try:
        # Client().pull returns a ChatPromptTemplate
        logger.info(f"Attempting to pull prompt from LangChain Hub: {prompt_handle}")
        client = Client()
        prompt = client.pull(prompt_handle)
        return prompt
    except Exception as e:
        logger.warning(f"Failed to pull prompt '{prompt_handle}' from Hub: {e}. Using fallback prompt.")
        return ChatPromptTemplate.from_messages([
            ("system", FALLBACK_SYSTEM_PROMPT),
            ("placeholder", "{messages}")
        ])
