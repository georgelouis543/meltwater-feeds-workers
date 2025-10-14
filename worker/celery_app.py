from datetime import timedelta

from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
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