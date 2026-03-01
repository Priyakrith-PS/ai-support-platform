from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.ticket import TicketCreate, TicketOut
from uuid import uuid4

from app.models.ticket_message import TicketMessage
from app.schemas.ticket_message import TicketMessageCreate, TicketMessageOut
from app.models.ai_response import AIResponse
from app.schemas.conversation import ConversationMessage



router = APIRouter(prefix="/tickets", tags=["Tickets"])


# ✅ Create Ticket
@router.post("/", response_model=TicketOut)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_ticket = Ticket(
        id=str(uuid4()),
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        user_id=current_user.id,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket



# ✅ Get My Tickets
@router.get("/")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tickets = db.query(Ticket).filter(
        Ticket.user_id == current_user.id
    ).all()

    return tickets

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # ownership check
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return ticket

@router.post("/{ticket_id}/messages", response_model=TicketMessageOut)
def send_message(
    ticket_id: str,
    data: TicketMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    message = TicketMessage(
        id=str(uuid4()),
        ticket_id=ticket_id,
        sender_id=current_user.id,
        message=data.message,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

@router.get("/{ticket_id}/messages", response_model=list[TicketMessageOut])
def get_ticket_messages(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Check ticket exists
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Ensure user owns this ticket
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")

    messages = db.query(TicketMessage)\
        .filter(TicketMessage.ticket_id == ticket_id)\
        .order_by(TicketMessage.created_at)\
        .all()

    return messages

@router.get("/{ticket_id}/conversation", response_model=list[ConversationMessage])
def get_conversation(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Check ticket exists
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Ensure the ticket belongs to the logged-in user
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")

    user_messages = db.query(TicketMessage).filter(
        TicketMessage.ticket_id == ticket_id
    ).all()

    ai_messages = db.query(AIResponse).filter(
        AIResponse.ticket_id == ticket_id
    ).all()

    conversation = []

    for msg in user_messages:
        conversation.append({
            "sender": "user",
            "message": msg.message,
            "created_at": msg.created_at,
            "confidence": None
        })

    for resp in ai_messages:
        conversation.append({
            "sender": "ai",
            "message": resp.response,
            "created_at": resp.created_at,
            "confidence": resp.confidence
        })

    conversation.sort(key=lambda x: x["created_at"])

    return conversation