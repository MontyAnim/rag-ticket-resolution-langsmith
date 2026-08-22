from typing import Any, Dict
from pydantic import BaseModel, Field
from langsmith.schemas import Run, Example
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI # Ready for OpenAI integration
from src.core.config import settings

class EvalResult(BaseModel):
    score: float = Field(description="Score between 0.0 and 1.0 (1.0 = pass, 0.0 = fail).")
    reasoning: str = Field(description="Brief explanation of why this score was given.")

# To switch to OpenAI for production/portfolio, uncomment the following line and comment out ChatGroq
# judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0).with_structured_output(EvalResult)

judge_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.0).with_structured_output(EvalResult)

PRECISION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an impartial judge evaluating an AI agent's response against an expected behavior.\n"
               "Score 1.0 if the agent followed the expected behavior completely.\n"
               "Score 0.0 if the agent failed to follow it.\n"
               "Return ONLY your score and reasoning in the requested structured format."),
    ("human", "Expected Behavior: {expected}\n\nAgent's Actual Response: {actual}")
])

FAITHFULNESS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an impartial judge. Your task is to detect hallucinations.\n"
               "Score 1.0 if the agent's response is completely factual, admits ignorance when lacking context, and does not invent policies or tool outputs.\n"
               "Score 0.0 if the agent invents information not present in its knowledge base or prompt.\n"
               "Return ONLY your score and reasoning in the requested structured format."),
    ("human", "Agent's Response: {actual}")
])

def precision_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates whether the agent's response matches the expected behavior.
    """
    # Extract actual output
    messages = run.outputs.get("messages", []) if run.outputs else []
    if messages:
        last_msg = messages[-1]
        actual_output = last_msg.get("content", "") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
    else:
        actual_output = str(run.outputs)
    
    # Extract expected behavior from the Golden Dataset
    expected_behavior = example.outputs.get("expected_behavior", "") if example.outputs else ""
    
    chain = PRECISION_PROMPT | judge_llm
    result: EvalResult = chain.invoke({
        "expected": expected_behavior,
        "actual": actual_output
    })
    
    return {
        "key": "precision",
        "score": result.score,
        "comment": result.reasoning
    }

def faithfulness_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates whether the agent hallucinates or invents information.
    """
    messages = run.outputs.get("messages", []) if run.outputs else []
    if messages:
        last_msg = messages[-1]
        actual_output = last_msg.get("content", "") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
    else:
        actual_output = str(run.outputs)
    
    chain = FAITHFULNESS_PROMPT | judge_llm
    result: EvalResult = chain.invoke({
        "actual": actual_output
    })
    
    return {
        "key": "faithfulness",
        "score": result.score,
        "comment": result.reasoning
    }

TONE_RELEVANCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an impartial judge evaluating a customer support agent's response.\n"
               "Your task is to determine two things:\n"
               "1. Did the agent address the user's primary question or issue? (Relevance)\n"
               "2. Is the agent's tone professional, polite, and free of condescension or toxicity? (Tone)\n"
               "Score 1.0 if the response is both relevant and maintains a polite/professional tone.\n"
               "Score 0.0 if the response fails to address the question OR if the tone is toxic/condescending.\n"
               "Return ONLY your score and reasoning in the requested structured format."),
    ("human", "User's Query: {user_query}\n\nAgent's Response: {actual}")
])

def tone_and_relevance_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates whether the response is relevant to the user's query and maintains a professional tone.
    """
    messages = run.outputs.get("messages", []) if run.outputs else []
    if messages:
        last_msg = messages[-1]
        actual_output = last_msg.get("content", "") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
    else:
        actual_output = str(run.outputs)
        
    user_inputs = run.inputs.get("messages", []) if run.inputs else []
    if user_inputs:
        first_msg = user_inputs[0]
        user_query = first_msg.get("content", "") if isinstance(first_msg, dict) else getattr(first_msg, "content", str(first_msg))
    else:
        user_query = str(run.inputs)
    
    chain = TONE_RELEVANCE_PROMPT | judge_llm
    result: EvalResult = chain.invoke({
        "user_query": user_query,
        "actual": actual_output
    })
    
    return {
        "key": "tone_and_relevance",
        "score": result.score,
        "comment": result.reasoning
    }
