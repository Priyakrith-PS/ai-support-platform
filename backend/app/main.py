from fastapi import FastAPI
from app.api import users, auth
from app.db.session import engine
from app.db.base import Base
from app.models import user

# IMPORTANT: import models so SQLAlchemy registers tables
from app.models import user  

app = FastAPI(title="AI Support Platform")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"status": "ok"}
