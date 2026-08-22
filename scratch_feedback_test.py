from langsmith import Client
from src.core.config import settings
import httpx
import asyncio

async def main():
    print("Fetching latest run from LangSmith...")
    client = Client()
    runs = list(client.list_runs(project_name="Rag-Ops Support Engine", limit=1))
    
    if not runs:
        print("No runs found in LangSmith. Ensure LANGSMITH_TRACING is enabled.")
        return
        
    latest_run_id = str(runs[0].id)
    print(f"Got latest run ID: {latest_run_id}")
    
    # 3. Send feedback via our API
    print("Sending feedback via API...")
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(
                "http://localhost:8000/api/v1/feedback",
                json={
                    "trace_id": latest_run_id,
                    "score": 0.0,
                    "comment": "Test feedback ingestion API."
                }
            )
            print(f"API Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to connect to FastAPI: {e}")

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
