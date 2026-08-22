from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
from langsmith import Client
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
client = Client()

class FeedbackRequest(BaseModel):
    trace_id: str
    score: float
    comment: Optional[str] = None

def submit_feedback_to_langsmith(trace_id: str, score: float, comment: Optional[str]):
    try:
        client.create_feedback(
            run_id=trace_id,
            key="user_score",
            score=score,
            comment=comment
        )
        logger.info(f"Successfully submitted feedback for trace {trace_id}")
    except Exception as e:
        logger.error(f"Failed to submit feedback for trace {trace_id}: {e}")

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest, background_tasks: BackgroundTasks):
    """
    Ingests user feedback and asynchronously sends it to LangSmith
    to avoid blocking the main event loop.
    """
    background_tasks.add_task(
        submit_feedback_to_langsmith,
        request.trace_id,
        request.score,
        request.comment
    )
    return {"status": "ok", "message": "Feedback received"}
