import logging

from worker.config.database import (
    feed_collection,
    documents_collection,
    cache_collection
)
from worker.controllers.html_to_rss.update_feed_controller import update_existing_feed


async def get_feed_params():
    feeds_cursor = feed_collection.find({
        "feed_type": "html_to_rss"
    })
    feeds = await feeds_cursor.to_list(length=None)

    for feed_params in feeds:
        try:
            feed_id = str(feed_params["_id"])
            logging.info(f"Updating feed: {feed_id}")

            await update_existing_feed(
                feed_params,
                documents_collection,
                cache_collection
            )

        except Exception as e:
            logging.warning(f"Error updating feed {feed_params['_id']}: {e}")
            continue

    logging.info("All feeds updated successfully.")