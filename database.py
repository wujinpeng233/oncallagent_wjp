from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

DATABASE_URL ="mysql+pymysql://oncall:oncall@127.0.0.1:3306/oncall_agent"

engine = create_engine(DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)

class Base(DeclarativeBase):
    pass