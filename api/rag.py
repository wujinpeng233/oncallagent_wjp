
from rag.qa_service import answer_question
from schemas.rag import RagAnswer,RagQuestion
from pathlib import Path
from fastapi import APIRouter,File,HTTPException,UploadFile
from rag.index_service import index_document
from schemas.rag import DocumentIndexRequest

router = APIRouter(prefix="/rag", tags=["rag"])

@router.post("/query",response_model=RagAnswer)
def query_knowledge(data:RagQuestion):
    return answer_question(data.question)

@router.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400,detail="No file name")

    file_name =Path(file.filename.replace("\\","/")).name

    if Path(file_name).suffix.lower() not in {".md",".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only .md and .txt files are allowed"
        )

    content = await file.read(5*1024*1024+1)
    if len(content) > 5*1024*1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 5MB limit"
        )
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="File must be UTF-8 encoding"

        )   from exc


    project_root = Path(__file__).resolve().parent.parent
    knowledge_dir = project_root / "knowledge"
    knowledge_dir.mkdir(parents=True,exist_ok=True)

    destination = knowledge_dir / file_name
    if destination.exists():
        raise HTTPException(
            status_code=400,
            detail="File already exists"
        )

    destination.write_text(text,encoding="utf-8")
    try:
        chunk_count = index_document(destination)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"File was saved,but indexing failed:{type(exc).__name__}"
        )   from exc
    return{
        "filename": file_name,
        "characters": len(text),
        "message": "File uploaded successfully",
        "chunk_count": chunk_count,
    }

@router.post("/documents/reindex")
def reindex_document(data: DocumentIndexRequest):
    knowledge_dir = (
        Path(data.file_path).resolve().parent.parent / "knowledge"
    ).resolve()

    file_name = data.file_name

    if(
        Path(file_name).name != file_name
        or "/" in file_name
        or "\\" in file_name
    ):
        raise HTTPException(
            status_code=400,
            detail="Only a file name is allowed",
        )

    destination = (knowledge_dir / file_name).resolve()

    if destination.parent != knowledge_dir:
        raise HTTPException(
            status_code=400,
            detail="Invalid file path",
        )

    if destination.suffix.lower() not in {".md",".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only .md and .txt files are allowed"
        )

    if not destination.is_file():
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    try:
        chunk_count = index_document(destination)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"File was indexed,but indexing failed:{type(exc).__name__}"
        )   from exc

    return{
        "filename": file_name,
        "chunk_count": chunk_count,
        "message": "File reindexed successfully",
    }


