import json
from pathlib import Path

from rag.embedding_service import create_embedding_service
from rag.vector_store import create_vector_store


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent

    embeddings = create_embedding_service()
    store = create_vector_store(
        embeddings,
        database_path=str(project_root / "data/oncall_agent.db"),
    )

    old_source = (
        "C:/Users/30521/Desktop/猛攻offfer/oncall-agent/"
        "knowledge/database-connection.md"
    )

    old_expr = f"source == {json.dumps(old_source, ensure_ascii=False)}"
    old_ids = store.get_pks(expr=old_expr) or []

    if not old_ids:
        print("No old chunks to clean up.")
        print("Cleanup completed")
        raise SystemExit(0)

    print("Old chunks:", len(old_ids))

    if not store.delete(ids=old_ids):
        raise RuntimeError("Old index cleanup failed")

    remaining = store.get_pks(expr=old_expr) or []
    if remaining:
        raise RuntimeError("Old chunks still exist")

    print("Remaining old chunks:", len(remaining))
    print("Cleanup completed")