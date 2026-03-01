from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(String(36), primary_key=True, index=True)

    ticket_id = Column(String(36), ForeignKey("tickets.id"))
    sender_id = Column(String(36), ForeignKey("users.id"))

    message = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    ticket = relationship("Ticket", backref="messages")
    sender = relationship("User")