from celery import Celery

from app.config import settings
from app.tasks.schedules import beat_schedule


celery_app = Celery(
    "ai_media_watch",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.collection"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
    beat_schedule=beat_schedule(),
)

