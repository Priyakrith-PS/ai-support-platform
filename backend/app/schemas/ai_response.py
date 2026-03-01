from pydantic import BaseModel


class AIResponseCreate(BaseModel):
    ticket_id: str
    user_message_id: str
    response: str
    confidence: float | None = None
    model_version: str | None = None


class AIResponseOut(BaseModel):
    id: str
    ticket_id: str
    user_message_id: str
    response: str
    confidence: float | None
    model_version: str | None

    class Config:
        from_attributes = True