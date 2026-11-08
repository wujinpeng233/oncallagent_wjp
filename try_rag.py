from rag.document_splitter import split_markdown_file
from rag.embedding_service import create_embedding_service
from rag.file_reader import read_text_file
from rag.vector_store import (
    create_vector_store,
    save_documents,
    search_documents,
)
from rag.context_builder import build_context
from rag.answer_service import create_chat_model, generate_answer
from rag.qa_service import answer_question

if __name__ == "__main__":
    embeddings = create_embedding_service()
    vector_store = create_vector_store(embeddings)

    # 库为空时才入库，避免重复运行导致向量重复
    collection_name = "runbook_chunks"
    chunk_count = 0
    if vector_store.client.has_collection(collection_name):
        chunk_count = vector_store.client.query(
            collection_name=collection_name,
            filter="source != ''",
            output_fields=["count(*)"],
        )[0]["count(*)"]

    if chunk_count == 0:
        path, content = read_text_file("knowledge/database-connection.md")
        documents = split_markdown_file(content, path)

        saved_ids = save_documents(vector_store, documents)
        print(f"saved ids: {saved_ids}")
    else:
        print("documents already ingested, skip")

    # query = "数据库连接失败怎么排查？"
    # results = search_documents(vector_store, query, k=3)
    #
    # print(f"query: {query}")
    # print(f"results: {len(results)}")
    #
    # for index, document in enumerate(results):
    #     print(f"\n--- result {index} ---")
    #     print("metadata:", document.metadata)
    #     print(document.page_content)
    #
    # results = search_documents(vector_store, query, k=3)
    #
    # context, citations = build_context(results)
    #
    # print("检索上下文：")
    # print(context)
    # print("\n引用信息：")
    # print(citations)
    #
    # chat_model = create_chat_model()
    # answer = generate_answer(chat_model, query, context)
    #
    # print("\n生成回答：")
    # print(answer)
    question=input()
    result = answer_question(question)
    print("\n回答：")
    print(result["answer"])
    print("\n引用：")
    print(result["citations"])