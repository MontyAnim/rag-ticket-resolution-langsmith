import asyncio
import argparse
from langsmith import Client, aevaluate
from langchain_core.messages import HumanMessage
from src.agent.graph import get_agent_graph
from src.evals.heuristic import latency_evaluator, tokens_evaluator
from src.evals.llm_judge import precision_evaluator, faithfulness_evaluator, tone_and_relevance_evaluator

async def run_target(inputs: dict) -> dict:
    """
    Adapter function that takes the inputs from the LangSmith dataset Example,
    runs the agent pipeline, and returns the output to be evaluated.
    """
    user_query = ""
    messages = inputs.get("messages", [])
    if messages and isinstance(messages, list):
        user_query = messages[-1].get("content", "")
    if not user_query:
        # Fallback if the dataset was seeded differently
        user_query = str(inputs)
        
    graph = get_agent_graph()
    
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "user_id": "test_user_eval",
        "tenant_id": "test_tenant_eval"
    }
    
    # Run the graph
    result = await graph.ainvoke(initial_state)
    
    # We return the final state, which langsmith will pass to our evaluators as run.outputs
    # Our evaluators already know how to extract `run.outputs.get("messages", [])[-1].content`
    return result

async def main():
    parser = argparse.ArgumentParser(description="Run CI/CD Evaluators against Golden Dataset")
    parser.add_argument("--dataset", type=str, default="Support Agent Golden Dataset", help="Name of the LangSmith dataset")
    parser.add_argument("--prefix", type=str, default="CI-CD-Eval", help="Prefix for the experiment run name")
    args = parser.parse_args()

    client = Client()
    
    evaluators = [
        latency_evaluator,
        tokens_evaluator,
        precision_evaluator,
        faithfulness_evaluator,
        tone_and_relevance_evaluator
    ]
    
    print(f"Starting evaluation on dataset: '{args.dataset}'")
    print(f"Using {len(evaluators)} evaluators. This will take a moment...")
    
    experiment_results = await aevaluate(
        run_target,
        data=args.dataset,
        evaluators=evaluators,
        experiment_prefix=args.prefix,
        client=client
    )
    
    print("\n==============================")
    print("      EVALUATION COMPLETE     ")
    print("==============================\n")
    print(f"Experiment Name: {experiment_results.experiment_name}")
    print(f"Results Link: {experiment_results.get_url()}")

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
