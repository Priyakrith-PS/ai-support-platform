from google import genai
from app.core.config import settings


print("settings key =", settings.google_api_key[:15], "...")

client = genai.Client(api_key=settings.google_api_key)


def generate_answer(query, docs, chat_history=""):
    context = "\n".join(docs)

    prompt = f"""
You are a helpful IT support assistant.

Conversation History:
{chat_history}

Knowledge Base:
{context}

User Question:
{query}

Instructions:
- Answer clearly and step-by-step
- Use conversation history if needed
- If user refers to previous issue, continue context
- NEVER abruptly say "I don't know"
- If unsure, guide the user

IMPORTANT:
- ALWAYS end your answer with:
"Did this solve your issue?"

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text