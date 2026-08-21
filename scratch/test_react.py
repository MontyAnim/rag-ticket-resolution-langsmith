import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool

load_dotenv()

@tool
def retrieve_knowledge(query: str) -> str:
    """Search knowledge base"""
    return "knowledge"

@tool
def query_ticket_status(query: str) -> str:
    """Check ticket status"""
    return "status"

TOOLS = [retrieve_knowledge, query_ticket_status]

async def test():
    llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0.0)
    llm_with_tools = llm.bind_tools(TOOLS)
    
    messages = [
        SystemMessage(content="You are a helpful support agent."),
        HumanMessage(content="What is the refund policy?")
    ]
    try:
        response = await llm_with_tools.ainvoke(messages)
        print("Response:", response)
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
