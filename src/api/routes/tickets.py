import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.graph import get_agent_graph
from src.agent.checkpointer import get_checkpointer
from src.core.database import get_db
from src.core.config import settings
from src.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

class TicketRequest(BaseModel):
    query: str = Field(..., description="The user query or issue description")
    user_id: str = Field(..., description="The ID of the user submitting the ticket")
    tenant_id: str = Field(..., description="The tenant ID for multi-tenant data isolation")
    thread_id: str | None = Field(default=None, description="Optional LangGraph thread ID for continuing past conversations")

class TicketResponse(BaseModel):
    thread_id: str
    intent: str | None
    response: str

@router.post("/process", response_model=TicketResponse)
async def process_ticket(payload: TicketRequest, db: AsyncSession = Depends(get_db)):
    """
    Receives a support query, runs the LangGraph AI workflow with persistent PostgreSQL memory,
    and returns the final response.
    """
    thread_id = payload.thread_id or f"thread_{uuid.uuid4().hex[:8]}"
    
    # Configure graph runtime parameters and LangSmith telemetry
    config = {
        "configurable": {
            "thread_id": thread_id,
            "tenant_id": payload.tenant_id,
            "user_id": payload.user_id
        },
        "metadata": {
            "tenant_id": payload.tenant_id,
            "user_id": payload.user_id,
            "thread_id": thread_id,
            "ls_provider": settings.LLM_PROVIDER,
            "ls_model_name": settings.LLM_MODEL_NAME,
            "backend_version": settings.VERSION
        },
        "tags": [
            f"tenant:{payload.tenant_id}",
            "source:api",
            f"env:{settings.ENVIRONMENT}",
            "tool:support_agent"
        ]
    }
    
    input_state = {
        "messages": [HumanMessage(content=payload.query)],
        "user_id": payload.user_id,
        "tenant_id": payload.tenant_id
    }
    
    try:
        async with get_checkpointer() as checkpointer:
            graph = get_agent_graph(checkpointer=checkpointer)
            final_state = await graph.ainvoke(input_state, config=config)
            
            # Extract last AI response
            messages = final_state.get("messages", [])
            ai_messages = [m for m in messages if isinstance(m, AIMessage)]
            last_response = ai_messages[-1].content if ai_messages else "No response generated."
            intent = final_state.get("current_intent")

            # Ensure user exists to prevent ForeignKeyViolationError
            from src.models.user import User
            from sqlalchemy.future import select
            
            user_record = await db.execute(select(User).where(User.id == payload.user_id))
            if not user_record.scalar_one_or_none():
                new_user = User(id=payload.user_id, tenant_id=payload.tenant_id)
                db.add(new_user)
                await db.flush()

            # Persist ticket record for auditing
            ticket = Ticket(
                tenant_id=payload.tenant_id,
                user_id=payload.user_id,
                thread_id=thread_id,
                query=payload.query
            )
            db.add(ticket)
            await db.commit()

            return TicketResponse(
                thread_id=thread_id,
                intent=intent,
                response=str(last_response)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent workflow: {str(e)}")
