from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Support Platform"
    env: str = "development"

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
