from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    response_id: str
    rating: int
    corrected_answer: str | None = None
    comment: str | None = None