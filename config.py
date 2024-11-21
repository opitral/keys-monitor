from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///keys.db"
    LOGGING_FILE: str = "keylogger.log"
    BOT_TOKEN: str
    ADMINS: list[int]
    SHOW_FIELDS: list[str]

    class Config:
        env_file = ".env"


settings = Settings()
