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


@router.post("/{ticket_id}/messages", response_model=TicketMessageOut)
def send_message(
    ticket_id: str,
    data: TicketMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
    messages = db.query(TicketMessage)\
        .filter(TicketMessage.ticket_id == ticket_id)\
        .order_by(TicketMessage.created_at)\
        .all()

    return messages