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
    include=[
        "worker.tasks.html_to_rss_feeds_task",
        "worker.tasks.rss_playground_task"
    ],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


celery_app.conf.beat_schedule = {
    "html-to-rss-worker": {
        "task": "worker.tasks.html_to_rss_feeds_task.run_all_feeds",
        "schedule": timedelta(minutes=30),
        "options": {
            "queue": "html_to_rss"
        },
    },

    "rss-playground-worker": {
        "task": "worker.tasks.rss_playground_task.run_all_feeds",
        "schedule": timedelta(minutes=30),
        "options": {
            "queue": "rss_playground"
        },
    }
}