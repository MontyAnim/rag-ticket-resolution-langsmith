from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from src.core.config import settings

@asynccontextmanager
async def get_checkpointer():
    """
    Context manager that yields an AsyncPostgresSaver for LangGraph.
    It automatically formats the DATABASE_URL to use the native psycopg driver
    and ensures that the required checkpoint tables exist in the database.
    """
    # LangGraph's checkpointer uses psycopg natively, not asyncpg.
    # Therefore, we remove the +asyncpg dialect if it's present.
    conn_string = settings.DATABASE_URL.replace("+asyncpg", "")
    
    async with AsyncPostgresSaver.from_conn_string(conn_string) as checkpointer:
        # Setup automatically creates checkpoints, checkpoint_blobs, and checkpoint_writes tables if they don't exist
        await checkpointer.setup()
        yield checkpointer
