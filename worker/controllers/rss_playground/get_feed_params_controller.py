import logging

from worker.config.database import get_database
from worker.controllers.rss_playground.update_feed_controller import update_existing_feed


async def get_feed_params():
    client, db = get_database()

    feed_collection = db["feed_collection"]
    documents_collection = db["documents_collection"]
    render_cache_collection = db["render_cache"]

    feeds_cursor = feed_collection.find({
        "feed_type": "rss_to_mwfeed"
    })
    feeds = await feeds_cursor.to_list(length=None)

    for feed_params in feeds:
        try:
            feed_id = str(feed_params["_id"])
            logging.info(f"Updating feed: {feed_id}")

            await update_existing_feed(
                feed_params,
                documents_collection,
                render_cache_collection
            )

        except Exception as e:
            logging.warning(f"Error updating feed {feed_params['_id']}: {e}")
            continue

    logging.info("All feeds updated successfully.")