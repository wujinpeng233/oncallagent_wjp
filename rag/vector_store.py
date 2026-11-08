from pathlib import Path
from threading import Lock

from langchain_milvus import Milvus

_stores = {}
_stores_lock = Lock()

def create_vector_store(
        embedding_service,
        database_path: str ="data/oncall_agent.db"
):
    key = str(Path(database_path).resolve())

    with _stores_lock:
        store = _stores.get(key)
        if store is not None:
            return store

        path = Path(database_path)
        path.parent.mkdir(parents=True,exist_ok=True)

        store = Milvus(
            embedding_function=embedding_service,
            collection_name="runbook_chunks",
            connection_args={
                "uri":str(path),
                "grpc_options": {
                    "grpc.keepalive_permit_without_calls": False,
                    "grpc.keepalive_time_ms": 3600000,
                },
            },
            index_params={
                "index_type":"AUTOINDEX",
                "metric_type": "COSINE",
            },
            auto_id=True,
        )
        _stores[key] = store
        return store

def save_documents(vector_store,documents):
    if not documents:
        return []

    return  vector_store.add_documents(documents)

def search_documents(vector_store,query:str,k:int =3):
    if not query.strip():
        raise ValueError("query cannot be empty")
    if k <= 0:
        raise ValueError("k must be greater than 0")

    return  vector_store.similarity_search(query,k=k)