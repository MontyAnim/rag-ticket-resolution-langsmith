from langsmith.schemas import Run, Example
from typing import Dict, Any

MAX_LATENCY_SECONDS = 15.0
MAX_TOKENS = 1500

def latency_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates if the run took less than MAX_LATENCY_SECONDS.
    """
    if run.start_time and run.end_time:
        latency = (run.end_time - run.start_time).total_seconds()
        score = 1.0 if latency < MAX_LATENCY_SECONDS else 0.0
        return {
            "key": "latency",
            "score": score,
            "comment": f"Latency was {latency:.2f}s"
        }
    return {
        "key": "latency",
        "score": 0.0,
        "comment": "Start or end time missing"
    }

def tokens_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates if the total token count is less than MAX_TOKENS.
    """
    tokens = 0
    prompt_tokens = getattr(run, "prompt_tokens", None)
    completion_tokens = getattr(run, "completion_tokens", None)
    total_tokens = getattr(run, "total_tokens", None)

    if prompt_tokens is not None and completion_tokens is not None:
        tokens = prompt_tokens + completion_tokens
    elif total_tokens is not None:
        tokens = total_tokens
    
    score = 1.0 if tokens < MAX_TOKENS else 0.0
    return {
        "key": "token_usage",
        "score": score,
        "comment": f"Used {tokens} tokens"
    }

import json

def json_format_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Evaluates whether a specific string output is valid JSON, if expected.
    """
    expected_format = example.outputs.get("format", "") if example.outputs else ""
    
    if expected_format.lower() != "json":
        return {"key": "json_format", "score": 1.0, "comment": "JSON format not required"}

    messages = run.outputs.get("messages", []) if run.outputs else []
    if messages:
        last_msg = messages[-1]
        actual_output = last_msg.get("content", "") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
    else:
        actual_output = str(run.outputs)

    try:
        json.loads(actual_output)
        return {"key": "json_format", "score": 1.0, "comment": "Output is valid JSON."}
    except json.JSONDecodeError as e:
        return {"key": "json_format", "score": 0.0, "comment": f"Output is invalid JSON: {e}"}

def tool_invocation_evaluator(run: Run, example: Example) -> Dict[str, Any]:
    """
    Verifies that the required tools were invoked during the agent's execution.
    """
    required_tools = example.outputs.get("required_tools", []) if example.outputs else []
    
    if not required_tools:
        return {"key": "tool_invocation", "score": 1.0, "comment": "No tools required."}

    invoked_tools = set()
    if run.child_runs:
        for child in run.child_runs:
            if child.run_type == "tool":
                invoked_tools.add(child.name)
                
    missing_tools = [tool for tool in required_tools if tool not in invoked_tools]
    
    if missing_tools:
        return {
            "key": "tool_invocation",
            "score": 0.0,
            "comment": f"Missing: {missing_tools}"
        }
    else:
        return {
            "key": "tool_invocation",
            "score": 1.0,
            "comment": f"Invoked all required: {required_tools}"
        }
