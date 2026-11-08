from fastapi import APIRouter

from schemas.messages import MessageCreate

router = APIRouter(prefix="/messages",tags=["messages"])

@router.post("/preview")
def preview_message(message:MessageCreate):
    return{"content":message.content}

