from pydantic import BaseModel
from datetime import datetime


class ConversationMessage(BaseModel):
    sender: str
    message: str
    created_at: datetime
    confidence: float | None = None