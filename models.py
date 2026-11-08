from datetime import datetime,timezone


from sqlalchemy import ForeignKey,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(String(50),unique=True)
    sessions:Mapped[list["ChatSession"]] = relationship(back_populates="user")

class ChatSession(Base):
    __tablename__ = "sessions"

    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(100))
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))

    user:Mapped["User"]=relationship(back_populates="sessions")
    messages:Mapped[list["Message"]]=relationship(back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id:Mapped[int]=mapped_column(primary_key=True)
    role:Mapped[str]=mapped_column(String(20))
    content:Mapped[str]=mapped_column(Text)
    session_id:Mapped[int]=mapped_column(ForeignKey("sessions.id"))
    created_at:Mapped[datetime]=mapped_column(default=datetime.utcnow)

    session:Mapped["ChatSession"]=relationship(back_populates="messages")