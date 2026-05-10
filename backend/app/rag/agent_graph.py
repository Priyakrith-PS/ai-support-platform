from typing import TypedDict
import uuid
import json

from app.rag.retriever import retrieve
from app.rag.generator import generate_answer
from app.models.ticket import Ticket
from app.models.chat_message import ChatMessage
from app.models.ai_response import AIResponse

from google import genai
from app.core.config import settings

import os

print("agentgraph GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))
print("agentgraph GEMINI_API_KEY =", os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=settings.google_api_key)


# 🔹 Graph State
class AgentState(TypedDict):
    query: str
    docs: list
    answer: str
    decision: dict
    ticket_id: str


# 🔹 1. Retrieval Node
def retrieve_node(state: AgentState):
    docs = retrieve(state["query"])
    return {"docs": docs}


# 🔹 2. Generation Node
def generate_node(state: AgentState):
    answer = generate_answer(state["query"], state["docs"])
    return {"answer": answer}


# 🔹 3. Decision Node (LLM-based)
def decision_node(state: AgentState):

    query = state["query"].lower()

    if "not working" in query or "still not working" in query:
        return {
            "decision": {
                "resolved": False,
                "confidence": 0.95,
                "reason": "Explicit failure"
            }
        }

    # 🔥 RULE-BASED OVERRIDE (VERY IMPORTANT)
    if any(x in query for x in ["how to", "what is", "explain", "steps"]):
        return {
            "decision": {
                "resolved": True,
                "confidence": 0.9,
                "reason": "General knowledge query"
            }
        }

    if any(x in query for x in ["not working", "issue", "error", "problem", "fail"]):
        return {
            "decision": {
                "resolved": False,
                "confidence": 0.8,
                "reason": "Technical issue detected"
            }
        }

    # 🔥 FALLBACK LLM
    prompt = f"""
Return ONLY JSON.

User Query: {state["query"]}
Answer: {state["answer"]}

{{
  "resolved": true or false,
  "confidence": number,
  "reason": "short"
}}
"""

    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        decision = json.loads(res.text)

    except Exception as e:
        print("DECISION ERROR:", e)

        decision = {
            "resolved": False,
            "confidence": 0.0,
            "reason": "LLM failed"
        }

    try:
        text = res.text.strip()

        # 🔥 CLEAN RESPONSE (important)
        text = text.replace("```json", "").replace("```", "").strip()

        decision = json.loads(text)

    except Exception as e:
        print("DECISION PARSE ERROR:", e)
        decision = {
            "resolved": True,  # safer default
            "confidence": 0.5,
            "reason": "Fallback safe default"
        }

    return {"decision": decision}


# 🔹 4. Ticket Node
def ticket_node(state: AgentState, db, user_id):
    ticket = Ticket(
        id=str(uuid.uuid4()),
        title=state["query"],
        description=state["answer"],
        status="open",
        priority="medium",
        user_id=user_id
    )

    db.add(ticket)
    db.commit()

    return {"ticket_id": ticket.id}