import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME")
    ENV = os.getenv("ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")

settings = Settings()
