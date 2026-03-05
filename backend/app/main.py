from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, auth, tickets, ai, feedback, chat
from app.db.session import engine
from app.db.base import Base

# IMPORTANT: import models so SQLAlchemy registers tables
from app.models import user, ticket  

app = FastAPI(
    title="AI Support Platform",
    description="AI-powered support system with authentication and ticketing",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 config (THIS is important for Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Create tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(users.router, tags=["Users"])
app.include_router(auth.router,  tags=["Auth"])
app.include_router(tickets.router,  tags=["Tickets"])
app.include_router(ai.router)
app.include_router(feedback.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "ok"}
