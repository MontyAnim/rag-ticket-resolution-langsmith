from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from src.agent.state import AgentState
from src.agent.llm import get_llm
from src.agent.prompts import get_react_prompt
from src.agent.tools.retriever import retrieve_knowledge
from src.agent.tools.sql import query_ticket_status

TOOLS = [retrieve_knowledge, query_ticket_status]

async def react_node(state: AgentState, config: RunnableConfig | None = None) -> dict:
    """
    Core ReAct agent node that processes support queries, decides whether to call tools,
    and returns response messages to update the conversation state.
    """
    llm = get_llm(temperature=0.0)
    
    # Dynamically extract provider and model for FinOps tracking
    provider = "groq" if "Groq" in type(llm).__name__ else "openai"
    model_name = getattr(llm, "model_name", "unknown")
    
    # Immutable injection via with_config
    llm_with_tools = llm.bind_tools(TOOLS).with_config(
        metadata={
            "ls_provider": provider,
            "ls_model_name": model_name
        }
    )
    
    prompt = get_react_prompt()
    
    # Render prompt with messages
    rendered_prompt = prompt.invoke({"messages": list(state.get("messages", []))})
    
    response = await llm_with_tools.ainvoke(rendered_prompt, config)
    return {"messages": [response]}
