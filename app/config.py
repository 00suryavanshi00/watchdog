

# from pydantic_settings import BaseSettings


# # everything's at one place 
# class Settings(BaseSettings):
#     OPENAI_API_KEY: str
#     OPENAI_MODEL_NAME: str = "gpt-4"
#     CELERY_BROKER_URL: str = "redis://localhost:6379/0"
#     GITHUB_TOKEN: str = ""
#     REDIS_HOST: str = "localhost"
#     REDIS_PORT: int = 6379
#     REDIS_DB: int = 0

#     class Config:
#         env_file = "app/.env"

# settings = Settings()


from celery import Celery
from redis import Redis
from .settings import settings

# Initialize Celery
celery_app = Celery("tasks", broker=settings.CELERY_BROKER_URL)
celery_app.autodiscover_tasks(["app.tasks.celery_tasks"])
celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIMEZONE,
    enable_utc=True,
)

# Initialize Redis
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # Automatically decode bytes to str
)


