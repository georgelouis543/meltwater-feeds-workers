import asyncio
import logging

from worker.config.database import get_database
from worker.controllers.html_to_rss.update_feed_controller import update_existing_feed


MAX_CONCURRENT_FEEDS = 10

async def get_feed_params():
    client, db = get_database()

    feed_collection = db["feed_collection"]
    documents_collection = db["documents_collection"]
    render_cache_collection = db["render_cache"]

    feeds_cursor = feed_collection.find({
        "feed_type": "html_to_rss"
    })
    feeds = await feeds_cursor.to_list(length=None)

    sem = asyncio.Semaphore(MAX_CONCURRENT_FEEDS)

    async def limited_update(feed_params):
        async with sem:
            feed_id = str(feed_params["_id"])
            logging.info(f"Updating feed: {feed_id}")
            try:
                await update_existing_feed(
                    feed_params,
                    documents_collection,
                    render_cache_collection
                )
                logging.info(f"Feed {feed_id} updated successfully.")
            except Exception as e:
                logging.warning(f"Error updating feed {feed_id}: {e}")

    await asyncio.gather(*(limited_update(feed) for feed in feeds))

    logging.info("All feeds updated (concurrently) successfully.")