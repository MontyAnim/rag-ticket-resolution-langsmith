from langsmith import Client
from src.evals.heuristic import latency_evaluator, tokens_evaluator
from src.core.config import settings

def test_evaluators():
    client = Client()
    runs = list(client.list_runs(project_name="Rag-Ops Support Engine", limit=1))
    if not runs:
        print("No runs found.")
        return
        
    run = runs[0]
    
    # We pass None for the Example object since the heuristic evaluators
    # don't actually need it for this simple implementation.
    print(f"Testing Run ID: {run.id}")
    
    latency_res = latency_evaluator(run, None)
    print(f"Latency Evaluator: {latency_res}")
    
    tokens_res = tokens_evaluator(run, None)
    print(f"Tokens Evaluator: {tokens_res}")

if __name__ == "__main__":
    test_evaluators()
