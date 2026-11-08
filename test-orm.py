from database import SessionLocal
from models import User, ChatSession, Message

with SessionLocal() as db:
    user = db.query(User).filter_by(username="demo").first()

    if user is None:
        user = User(username="demo")
        db.add(user)
        db.flush()

    chat_session = ChatSession(title="第一次测试", user_id=user.id)
    db.add(chat_session)
    db.flush()

    message = Message(
        role="user",
        content="你好，这是第一条数据库消息。",
        session_id=chat_session.id,
    )
    db.add(message)
    db.commit()

    messages = (
        db.query(Message)
        .filter_by(session_id=chat_session.id)
        .order_by(Message.created_at, Message.id)
        .all()
    )

    print(f"用户 ID：{user.id}")
    print(f"会话 ID：{chat_session.id}")
    for item in messages:
        print(f"{item.role}: {item.content}")