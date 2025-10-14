import asyncio
import logging

from worker.celery_app import celery_app
from worker.controllers.rss_playground.get_feed_params_controller import get_feed_params


@celery_app.task
def run_all_feeds():
    logging.info("Starting scheduled feed updates...")
    asyncio.run(get_feed_params())
    logging.info("Feed update task finished.")
