from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "medium"


class TicketOut(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True
