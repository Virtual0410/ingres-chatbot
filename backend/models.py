from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .db import Base

class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    issue = Column(Text)
    report_id = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))    # "user" or "bot"
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
