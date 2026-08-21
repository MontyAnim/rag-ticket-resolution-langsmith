import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

class IntentClassification(BaseModel):
    intent: Literal["technical", "billing", "escalate"] = Field(
        ...,
        description="Classify the user's latest message intent."
    )

llm = ChatGroq(model='openai/gpt-oss-120b', temperature=0)
structured_llm = llm.with_structured_output(IntentClassification)

query = "How do I configure the PostgreSQL database?"
result = structured_llm.invoke(query)
print("Result:", result)
