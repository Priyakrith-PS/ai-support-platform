from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.db.base import Base


class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String(36), primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text)

    status = Column(
        Enum(TicketStatus),
        default=TicketStatus.open
    )

    priority = Column(
        Enum(TicketPriority),
        default=TicketPriority.medium
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", backref="tickets")
