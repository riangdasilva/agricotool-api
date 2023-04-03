from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "agricotool-api"
    DB_URL: str = ""
    DB_NAME: str = ""


settings = Settings()
