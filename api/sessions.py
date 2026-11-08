from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field

from database import SessionLocal
from models import ChatSession,User,Message

router =APIRouter(prefix="/sessions",tags=["sessions"])

class SessionCreate(BaseModel):
    username:str=Field(min_length=1,max_length=50)
    title:str=Field(min_length=1,max_length=100)

class MessageCreate(BaseModel):
    role:str = Field(pattern="^(user|assistant)$")
    content:str =Field(min_length=1,max_length=2000)

@router.post("")
def create_session(data:SessionCreate):
    with SessionLocal() as db:
        user = db.query(User).filter_by(username=data.username).first()

        if user is None:
            user=User(username=data.username)
            db.add(user)
            db.flush()

        chat_session=ChatSession(title=data.title,user_id=user.id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        return{
            "id":chat_session.id,
            "title":chat_session.title,
            "user_id":chat_session.user_id
        }

@router.post("/{session_id}/messages")
def create_messages(session_id:int,data:MessageCreate):
    with SessionLocal() as db:
        chat_session = db.query(ChatSession).filter_by(id=session_id).first()
        if chat_session is None:
            raise HTTPException(status_code=404,detail="session is not found")

        message = Message(
            role=data.role,
            content=data.content,
            session_id=session_id
        )
        db.add(message)
        db.commit()
        db.refresh(message)


        return {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "session_id": message.session_id
        }

@router.get("/{session_id}/messages")
def list_messages(session_id:int):
    with SessionLocal() as db:
        chat_session=db.query(ChatSession).filter_by(id=session_id).first()
        if chat_session is None:
            raise HTTPException(status_code=404,detail="session is not found")

        messages =(
            db.query(Message)
            .filter_by(session_id=chat_session.id)
            .order_by(Message.created_at, Message.id)
            .all()
        )

        return[
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "session_id": message.session_id
            }
            for message in messages
        ]