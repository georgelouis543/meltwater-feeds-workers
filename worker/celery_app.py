import os
from datetime import timedelta

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
REDIS_BROKER = os.getenv("REDIS_BROKER")
REDIS_BACKEND = os.getenv("REDIS_BACKEND")

celery_app = Celery(
    "worker",
    broker=REDIS_BROKER,
    backend=REDIS_BACKEND,
    include=["worker.tasks.run_feeds_task"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


celery_app.conf.beat_schedule = {
    "run-feed-updates-every-30-mins": {
        "task": "worker.tasks.run_feeds_task.run_all_feeds",
        "schedule": timedelta(seconds=30),
    },
}