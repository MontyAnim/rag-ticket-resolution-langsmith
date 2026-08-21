from typing import Literal
from pydantic import BaseModel, Field
from src.agent.state import AgentState
from src.agent.llm import get_llm
from src.core.config import settings

class IntentClassification(BaseModel):
    """Schema for routing intents."""
    intent: Literal["technical", "billing", "escalate"] = Field(
        ...,
        description=(
            "Classify the user's latest message intent. "
            "'technical' for questions about software, databases, configuration, errors, or troubleshooting. "
            "'billing' for questions about refunds, payments, invoices, or subscriptions. "
            "'escalate' for general greetings, non-support chats, complaints, or explicit requests for a human."
        )
    )

def router_node(state: AgentState) -> dict:
    """
    Analyzes the conversation history and classifies the user's intent.
    Returns the intent to update the AgentState.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"current_intent": "escalate"}  # Fallback

    # Initialize the LLM with structured output to guarantee matching literal values
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(IntentClassification)
    
    try:
        # Classify the intent based on the messages
        result = structured_llm.invoke(messages)
        return {"current_intent": result.intent}
    except Exception as e:
        # Fallback if the LLM refuses to use the tool or crashes
        import logging
        logging.getLogger(__name__).warning(f"Router LLM failed, defaulting to 'escalate': {e}")
        return {"current_intent": "escalate"}
