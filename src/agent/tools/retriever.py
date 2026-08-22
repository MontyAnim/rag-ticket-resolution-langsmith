from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client.models import Filter, FieldCondition, MatchValue
from langsmith import get_current_run_tree
from src.core.vector_db import qdrant_client

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@tool
async def retrieve_knowledge(query: str, config: RunnableConfig) -> str:
    """
    Search the technical knowledge base and manuals for relevant solutions to resolve support tickets.
    """
    run_tree = get_current_run_tree()
    if run_tree:
        run_tree.add_tags(["tool:retrieve_knowledge"])

    # Extract tenant_id from configurable parameters to ensure strict multi-tenancy isolation
    configurable = config.get("configurable", {})
    tenant_id = configurable.get("tenant_id")
    
    if not tenant_id:
        if run_tree:
            run_tree.add_tags(["exception:missing_tenant"])
        return "Error: tenant_id is missing from execution context."

    # Compute dense query vector using local HuggingFace embedding model
    query_vector = await embeddings.aembed_query(query)
    
    # Strict geometric filter for tenant_id in Qdrant
    tenant_filter = Filter(
        must=[
            FieldCondition(
                key="tenant_id",
                match=MatchValue(value=tenant_id)
            )
        ]
    )
    
    search_results = await qdrant_client.query_points(
        collection_name="knowledge_base",
        query=query_vector,
        query_filter=tenant_filter,
        limit=3
    )
    
    if not search_results.points:
        if run_tree:
            run_tree.add_tags(["exception:no_results"])
        return "No relevant documentation found in the knowledge base."
        
    formatted_docs = []
    for hit in search_results.points:
        payload = hit.payload or {}
        content = payload.get("content", "")
        source = payload.get("source", "Unknown")
        formatted_docs.append(f"[Source: {source}]\n{content}")
        
    return "\n\n---\n\n".join(formatted_docs)
