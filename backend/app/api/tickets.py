from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.ticket import TicketCreate, TicketOut
from uuid import uuid4



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
