from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from datetime import datetime, timezone

from app.db.base import Base


class AIFeedback(Base):
    __tablename__ = "ai_feedback"

    id = Column(String(36), primary_key=True, index=True)

    response_id = Column(String(36), ForeignKey("ai_responses.id"))

    rating = Column(Integer)  
    # 1 = bad
    # 2 = okay
    # 3 = good

    corrected_answer = Column(Text, nullable=True)

    comment = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )