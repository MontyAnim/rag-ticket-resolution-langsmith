from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import AIMessage
from src.agent.state import AgentState
from src.agent.nodes.router import router_node
from src.agent.nodes.react import react_node
from src.agent.tools.retriever import retrieve_knowledge
from src.agent.tools.sql import query_ticket_status

TOOLS = [retrieve_knowledge, query_ticket_status]

def escalation_node(state: AgentState) -> dict:
    """
    Handles non-technical requests, billing inquiries, or human escalations.
    """
    intent = state.get("current_intent", "escalate")
    if intent == "billing":
        message = AIMessage(
            content="I have detected that your request is related to Billing. A representative from our Billing & Accounts department will review your case shortly."
        )
    else:
        message = AIMessage(
            content="Your request has been escalated to a human support specialist. An agent will follow up with you as soon as possible."
        )
    return {"messages": [message]}

def route_intent(state: AgentState) -> str:
    """
    Determines the next node based on the classified intent from the router node.
    """
    intent = state.get("current_intent", "escalate")
    if intent == "technical":
        return "agent"
    return "escalation"

def build_graph():
    """
    Constructs the uncompiled LangGraph StateGraph with all nodes, edges, and conditional branches.
    """
    workflow = StateGraph(AgentState)
    
    # 1. Register Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("agent", react_node)
    workflow.add_node("tools", ToolNode(TOOLS))
    workflow.add_node("escalation", escalation_node)
    
    # 2. Define Entrypoint
    workflow.add_edge(START, "router")
    
    # 3. Conditional routing from router node
    workflow.add_conditional_edges(
        "router",
        route_intent,
        {
            "agent": "agent",
            "escalation": "escalation"
        }
    )
    
    # 4. ReAct tool execution cycle
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )
    workflow.add_edge("tools", "agent")
    
    # 5. Escalation termination
    workflow.add_edge("escalation", END)
    
    return workflow

def get_agent_graph(checkpointer=None):
    """
    Compiles and returns the runnable LangGraph application.
    """
    workflow = build_graph()
    return workflow.compile(checkpointer=checkpointer)
