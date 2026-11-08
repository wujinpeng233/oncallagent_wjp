from pathlib import Path

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter,
)
def merge_small_chunks(
        chunks,
        min_size: int = 300,
        max_size: int = 1600,
):
    merged_chunks =[]
    for chunk in chunks:
        if(
            merged_chunks
            and len(merged_chunks[-1].page_content) < min_size
            and len(merged_chunks[-1].page_content)
            +2
            +len(chunk.page_content)
            <= max_size
        ):
            merged_chunks[-1].page_content +=(
                "\n\n" + chunk.page_content
            )
        else:
            merged_chunks.append(chunk)
    for index, chunk in enumerate(merged_chunks):
        chunk.metadata["chunk_id"] = index
    return merged_chunks
def split_markdown_file(
        content: str,
        source: Path,
):
    markdown_spliter =MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
        ],
        strip_headers=False,
    )

    sections =markdown_spliter.split_text(content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(sections)
    chunks = merge_small_chunks(
        chunks,
        min_size=300,
        max_size=1600,
    )
    for index, chunk in enumerate(chunks):
        chunk.metadata["source"] = source.as_posix()
        chunk.metadata["file_name"] = source.name
        chunk.metadata["chunk_id"] = index

    return chunks