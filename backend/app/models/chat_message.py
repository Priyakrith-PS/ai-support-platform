from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, index=True)

    session_id = Column(String(36), ForeignKey("chat_sessions.id"))

    sender = Column(String(20))  # user / ai

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    session = relationship("ChatSession", backref="messages")