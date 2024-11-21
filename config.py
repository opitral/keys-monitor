from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///keys.db"
    LOGGING_FILE: str = "keylogger.log"

    class Config:
        env_file = ".env"


settings = Settings()
