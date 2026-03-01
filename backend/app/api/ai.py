from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.models.ai_response import AIResponse
from app.schemas.ai_response import AIResponseCreate, AIResponseOut
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/respond", response_model=AIResponseOut)

def store_ai_response(
    data: AIResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    ai_response = AIResponse(
        id=str(uuid.uuid4()),
        ticket_id=data.ticket_id,
        message_id=data.user_message_id,
        response=data.response,
        confidence=data.confidence,
        model_version=data.model_version,
    )

    db.add(ai_response)
    db.commit()
    db.refresh(ai_response)

    return ai_response