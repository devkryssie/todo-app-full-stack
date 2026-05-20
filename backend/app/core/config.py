import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "todo_db"
    POSTGRES_HOST: str = "localhost"
    DATABASE_URL: Optional[str] = None

    JWT_SECRET_KEY: str = "9d268579fc93b6e824f0c9b0e271c6d17e750e1ef382b6b0d912df64273ab3bd"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"
    }

    def __init__(self, **values):
        super().__init__(**values)
        # Construct the database URL if not explicitly provided
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"

settings = Settings()
