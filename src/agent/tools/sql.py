from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from sqlalchemy import select
from src.core.database import AsyncSessionLocal
from src.models.ticket import Ticket

@tool
async def query_ticket_status(ticket_id: str | None = None, config: RunnableConfig = None) -> str:
    """
    Securely query the database for support ticket details or user ticket history.
    If ticket_id is provided, fetches that specific ticket. Otherwise, lists recent tickets for the current user.
    """
    config = config or {}
    configurable = config.get("configurable", {})
    tenant_id = configurable.get("tenant_id")
    user_id = configurable.get("user_id")

    if not tenant_id:
        return "Error: tenant_id is missing from execution context."

    async with AsyncSessionLocal() as session:
        # Build parameterized, injection-safe ORM query
        stmt = select(Ticket).where(Ticket.tenant_id == tenant_id)
        
        if ticket_id:
            stmt = stmt.where(Ticket.id == ticket_id)
        elif user_id:
            stmt = stmt.where(Ticket.user_id == user_id).limit(5)
        else:
            return "Error: Either ticket_id or user_id must be provided to query tickets."

        result = await session.execute(stmt)
        tickets = result.scalars().all()

        if not tickets:
            return "No tickets found matching the criteria."

        formatted_tickets = []
        for t in tickets:
            formatted_tickets.append(
                f"- Ticket ID: {t.id}\n  User ID: {t.user_id}\n  Query: {t.query}"
            )

        return "\n\n".join(formatted_tickets)
