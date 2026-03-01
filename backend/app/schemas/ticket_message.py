from pydantic import BaseModel
from datetime import datetime


class TicketMessageCreate(BaseModel):
    message: str


class TicketMessageOut(BaseModel):
    id: str
    ticket_id: str
    sender_id: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True