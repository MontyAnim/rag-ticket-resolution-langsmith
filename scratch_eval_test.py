import asyncio
from langsmith import Client
from langsmith.schemas import Example
from src.evals.llm_judge import precision_evaluator, faithfulness_evaluator
from src.core.config import settings

def test_llm_evaluators():
    client = Client()
    runs = list(client.list_runs(project_name="Rag-Ops Support Engine", limit=1))
    if not runs:
        print("No runs found.")
        return
        
    run = runs[0]
    
    # Let's mock the run outputs to ensure there's something to evaluate
    run.outputs = {"messages": [{"content": "I don't have enough context to answer that."}]}
    
    mock_example = Example(
        id="11111111-1111-1111-1111-111111111111",
        dataset_id="00000000-0000-0000-0000-000000000000",
        inputs={},
        outputs={"expected_behavior": "Agent should gracefully admit lack of context, avoid hallucinating solutions, and recommend escalating to Level 2 support."}
    )
    
    print(f"Testing Run ID: {run.id}")
    
    precision_res = precision_evaluator(run, mock_example)
    print(f"Precision Evaluator: {precision_res}")
    
    try:
        faithfulness_res = faithfulness_evaluator(run, mock_example)
        print(f"Faithfulness Evaluator: {faithfulness_res}")
    except UnicodeEncodeError:
        print("Faithfulness Evaluator completed, but reasoning contained special characters.")
        
    from src.evals.llm_judge import tone_and_relevance_evaluator
    run.inputs = {"messages": [{"content": "I am so angry! Answer my question right now! What is the capital of France?"}]}
    run.outputs = {"messages": [{"content": "Please calm down, the capital is Paris."}]}
    tone_res = tone_and_relevance_evaluator(run, mock_example)
    print(f"Tone & Relevance Evaluator: {tone_res}")

if __name__ == "__main__":
    test_llm_evaluators()
