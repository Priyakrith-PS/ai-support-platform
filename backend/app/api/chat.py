# app/api/chat.py

import uuid
import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from transformers import pipeline

from app.db.session import get_db
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.ai_response import AIResponse
from app.models.ticket import Ticket
from app.core.deps import get_current_user
from app.models.user import User

from app.rag.langgraph_agent import agent

router = APIRouter(prefix="/chat", tags=["Chat"])


# ======================================================
# LOAD FINE-TUNED MODEL (ONCE)
# Put final_support_model folder beside backend root
# ======================================================
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name
)

model = PeftModel.from_pretrained(
    base_model,
    "final_support_model"
)

ft_pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)


# ======================================================
# CREATE SESSION
# ======================================================
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


# ======================================================
# GET CHAT HISTORY
# ======================================================
@router.get("/session/{session_id}")
def get_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()

    return messages


# ======================================================
# MAIN CHAT
# ======================================================
@router.post("/send")
def chat_send(
    session_id: str,
    message: str,
    mode: str = "rag",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # --------------------------------------------------
    # VALIDATE SESSION
    # --------------------------------------------------
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).first()

    if not session:
        return {"error": "Invalid session_id"}

    # --------------------------------------------------
    # STORE USER MESSAGE
    # --------------------------------------------------
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender="user",
        message=message
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    lower_msg = message.lower()

    # --------------------------------------------------
    # CHECK LAST AI STATE
    # --------------------------------------------------
    last_ai_msg = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id,
        ChatMessage.sender == "ai"
    ).order_by(ChatMessage.created_at.desc()).first()

    awaiting_feedback = False
    awaiting_ticket = False

    if last_ai_msg:
        txt = last_ai_msg.message.lower()

        if "was this helpful" in txt:
            awaiting_feedback = True

        if "create a support ticket" in txt:
            awaiting_ticket = True

    yes_words = ["yes", "yeah", "yep", "ok", "sure"]
    no_words = ["no", "nah", "nope"]

    # ==================================================
    # CASE 1: FEEDBACK RESPONSE
    # ==================================================
    if awaiting_feedback:

        if any(w in lower_msg for w in yes_words):
            reply = "Great! Let me know if you need anything else."

        elif any(w in lower_msg for w in no_words):
            reply = "I'm sorry about that. Would you like me to create a support ticket? (yes/no)"

        else:
            reply = "Please reply yes or no. Was this helpful?"

    # ==================================================
    # CASE 2: TICKET RESPONSE
    # ==================================================
    elif awaiting_ticket:

        if any(w in lower_msg for w in yes_words):

            ticket = Ticket(
                id=str(uuid.uuid4()),
                title="User Issue",
                description=user_msg.message,
                status="open",
                priority="medium",
                user_id=current_user.id
            )

            db.add(ticket)
            db.commit()

            reply = "Your support ticket has been created successfully."

        elif any(w in lower_msg for w in no_words):
            reply = "Alright. Let me know if you need anything else."

        else:
            reply = "Please reply yes or no. Should I create a support ticket?"

    # ==================================================
    # CASE 3: NORMAL CHAT FLOW
    # ==================================================
    else:

        # Recent chat memory
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.desc()).limit(6).all()

        chat_history = "\n".join([
            f"{m.sender}: {m.message}" for m in reversed(messages)
        ])

        # ----------------------------------------------
        # MODE = RAG
        # ----------------------------------------------
        if mode == "rag":

            try:
                result = agent.invoke({
                    "query": message,
                    "chat_history": chat_history
                })

                answer = result["answer"]

            except Exception as e:
                answer = f"RAG service is temporarily unavailable.${repr(e)}"

        # ----------------------------------------------
        # MODE = FINE-TUNED
        # ----------------------------------------------
        else:

            prompt = f"""### Instruction:
{message}

### Response:
"""

            try:
                output = ft_pipe(
                    prompt,
                    max_new_tokens=180,
                    do_sample=False
                )[0]["generated_text"]

                answer = output.replace(prompt, "").strip()

            except Exception:
                answer = "Fine-tuned model unavailable."

        reply = answer + "\n\nWas this helpful? (yes/no)"

    # --------------------------------------------------
    # STORE AI MESSAGE
    # --------------------------------------------------
    ai_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender="ai",
        message=reply
    )

    db.add(ai_msg)

    # --------------------------------------------------
    # STORE AI RESPONSE
    # --------------------------------------------------
    ai_resp = AIResponse(
        id=str(uuid.uuid4()),
        ticket_id=None,
        message_id=user_msg.id,
        response=reply,
        confidence=json.dumps({})
    )

    db.add(ai_resp)
    db.commit()

    return {
        "reply": reply
    }