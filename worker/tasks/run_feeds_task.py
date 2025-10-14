from worker.celery_app import celery_app


@celery_app.task
def run_all_feeds():
    pass
