from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class AIResponse(Base):
    __tablename__ = "ai_responses"

    id = Column(String(36), primary_key=True, index=True)

    ticket_id = Column(String(36), ForeignKey("tickets.id"))
    message_id = Column(String(36), ForeignKey("ticket_messages.id"))

    response = Column(Text, nullable=False)

    confidence = Column(Float)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    ticket = relationship("Ticket")