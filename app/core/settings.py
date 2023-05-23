from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str = ""
    DB_NAME: str = "agricotool"
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
