import logging

from worker.controllers.html_to_rss.parser_controller import parse_input_html
from worker.controllers.items_controllers.save_items import save_items


async def update_existing_feed(
        feed_params,
        documents_collection,
        render_cache_collection,
) -> dict[str, str] | None:
    try:

        existing_feed_id = str(feed_params["_id"])

        get_items = await parse_input_html(
            feed_params,
            render_cache_collection
        )

        if get_items:
            save_items_res = await save_items(
                existing_feed_id,
                get_items,
                documents_collection
            )

            if save_items_res:
                return {
                    "message": f"Saved New items for Feed ID: {existing_feed_id}"
                }

            return {
                "message": f"No New items to save for Feed ID: {existing_feed_id}"
            }


    except Exception as e:
        logging.warning(f"An Exception {e} occurred while saving items")
        return {
            "message": f"An Exception {e} occurred while saving items!"
        }