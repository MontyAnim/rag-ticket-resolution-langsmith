from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    State representing the short-term memory of the LangGraph agent during a conversation.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_intent: Optional[str]
    user_id: str
    tenant_id: str
