from datetime import timedelta

from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
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
        "task": "worker.tasks.run_all_feeds",   # full import path to the task
        "schedule": timedelta(minutes=30),
    },
}