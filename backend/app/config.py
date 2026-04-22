from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    AI_API_KEY: str
    AI_API_BASE_URL: str
    FX_API_URL: str = "https://api.exchangerate.host/latest"

    class Config:
        env_file = ".env"

settings = Settings()
