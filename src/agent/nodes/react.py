from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from src.agent.state import AgentState
from src.agent.llm import get_llm
from src.agent.tools.retriever import retrieve_knowledge
from src.agent.tools.sql import query_ticket_status

TOOLS = [retrieve_knowledge, query_ticket_status]

async def react_node(state: AgentState, config: RunnableConfig | None = None) -> dict:
    """
    Core ReAct agent node that processes support queries, decides whether to call tools,
    and returns response messages to update the conversation state.
    """
    llm = get_llm(temperature=0.0)
    llm_with_tools = llm.bind_tools(TOOLS)
    
    system_prompt = SystemMessage(
        content=(
            "You are a helpful and precise technical support resolution assistant. "
            "Use the `retrieve_knowledge` tool to look up technical documentation and troubleshooting manuals. "
            "Use the `query_ticket_status` tool to check previous ticket history and details in the database. "
            "Always be polite, concise, and provide accurate answers based on the retrieved context."
        )
    )
    
    messages = [system_prompt] + list(state.get("messages", []))
    response = await llm_with_tools.ainvoke(messages, config)
    return {"messages": [response]}
