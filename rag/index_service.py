import json
from pathlib import Path

from rag.document_splitter import split_markdown_file
from rag.embedding_service import create_embedding_service
from rag.file_reader import read_text_file
from rag.vector_store import create_vector_store,save_documents

def index_document(file_path:Path) ->int:
    path,content = read_text_file(str(file_path))
    documents = split_markdown_file(content,path)

    if not documents:
        raise ValueError("documents produced no chunks")

    embeddings = create_embedding_service()
    vector_store = create_vector_store(embeddings)

    source = json.dumps(path.as_posix(),ensure_ascii=False)
    old_ids = vector_store.get_pks(
        expr=f"source == {source}"
    ) or []

    save_documents(vector_store,documents)

    if old_ids:
        deleted = vector_store.delete(old_ids)
        if not deleted:
            raise RuntimeError("New chunks saved, but old chunks cleanup failed")
    return len(documents)