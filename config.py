from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///keys.db"
    LOGGING_FILE: str = "keylogger.log"
    BOT_TOKEN: str
    ADMINS: list[int]
    SHOW_FIELDS: list[str]
    NOTIFICATION_TIME: str = "19:00"

    class Config:
        env_file = ".env"


settings = Settings()
