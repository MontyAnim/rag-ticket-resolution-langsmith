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
