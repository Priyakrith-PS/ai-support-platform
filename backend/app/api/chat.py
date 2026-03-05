import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.core.deps import get_current_user
from app.models.user import User


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/session")
def create_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    session = ChatSession(
        id=str(uuid.uuid4()),
        user_id=current_user.id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.post("/message")
def send_message(
    session_id: str,
    message: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender="user",
        message=message
    )

    db.add(msg)
    db.commit()

    return msg


@router.get("/session/{session_id}")
def get_messages(
    session_id: str,
    db: Session = Depends(get_db)
):

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()

    return messages