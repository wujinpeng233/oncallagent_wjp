from langchain_core.documents import Document

def build_context(
        documents: list[Document],
) -> tuple[str,list[dict]]:
    context_parts = []
    citations = []

    for index, document in enumerate(documents,start=1):
        file_name = document.metadata.get("file_name","unknown")
        source = document.metadata.get("source","unknown")
        chunk_id = document.metadata.get("chunk_id","unknown")

        context_parts.append(
            f"[{index}] 文件：{file_name}\n"
            f"来源：{source}\n"
            f"分块编号：{chunk_id}\n"
            f"内容：\n{document.page_content}"
        )

        citations.append(
            {
                "reference": index,
                "file_name": file_name,
                "source": source,
                "chunk_id": chunk_id,
                "content": document.page_content,
            }
        )

    return "\n\n".join(context_parts),citations