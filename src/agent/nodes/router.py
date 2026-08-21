from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.agent.state import AgentState
from src.core.config import settings

class IntentClassification(BaseModel):
    """Schema for routing intents."""
    intent: Literal["technical", "billing", "escalate"] = Field(
        ...,
        description="Classify the user's latest message intent."
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
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.0
    )
    structured_llm = llm.with_structured_output(IntentClassification)
    
    # Classify the intent based on the messages
    result = structured_llm.invoke(messages)
    
    # Return the dictionary to be merged into AgentState
    return {"current_intent": result.intent}
