import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.ticket import Ticket
from app.db.session import get_db
from app.models.ai_feedback import AIFeedback
from app.schemas.ai_feedback import FeedbackCreate

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/")
def submit_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):

    feedback = AIFeedback(
        id=str(uuid.uuid4()),
        response_id=data.response_id,
        rating=data.rating,
        corrected_answer=data.corrected_answer,
        comment=data.comment
    )

    db.add(feedback)

    # 🔥 NEW: if positive feedback → close ticket
    if data.rating == 1:
        ai_response = db.query(AIResponse).filter(
            AIResponse.id == data.response_id
        ).first()

        if ai_response and ai_response.ticket_id:
            ticket = db.query(Ticket).filter(
                Ticket.id == ai_response.ticket_id
            ).first()

            if ticket:
                ticket.status = "resolved"

    db.commit()

    return {"status": "feedback recorded"}