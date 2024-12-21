

from pydantic_settings import BaseSettings


# everything's at one place 
class Settings(BaseSettings):
    COHERE_API_KEY: str
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    GITHUB_TOKEN: str = ""
    GITHUB_WEBHOOK_SECRET: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    TIMEZONE: str = "UTC"


    class Config:
        env_file = "app/.env"

settings = Settings()

