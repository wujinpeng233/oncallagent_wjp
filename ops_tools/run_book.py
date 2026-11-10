from rag.context_builder import build_context
from rag.embedding_service import create_embedding_service
from rag.vector_store import create_vector_store,search_documents

def search_runbook(query: str) -> dict:
    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")

    embeddings = create_embedding_service()
    vector_store = create_vector_store(embeddings)

    documents = search_documents(vector_store,query,k=3)
    citations = build_context(documents)

    return {
        "query": query,
        "count": len(documents),
        "citations": citations,
    }