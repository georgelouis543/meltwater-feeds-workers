import logging

from worker.schema.document import ItemDocumentBase


async def save_items(
        feed_id: str,
        items: list[dict],
        documents_collection
) -> bool:

    existing_items_cursor = documents_collection.find(
        {
            "feed_id": feed_id
        },
        {
            "_id": 0,
            "item_url": 1
        }
    )
    existing_items = await existing_items_cursor.to_list(length=None)

    documents_to_insert = []

    if not existing_items:
        for item in items:
            try:
                 # Validate item using Pydantic
                document = ItemDocumentBase(
                    **item,
                    feed_id=feed_id
                )

                documents_to_insert.append(document.model_dump())

            except Exception as e:
                logging.warning(f"Skipping item due to error: {e}")
                continue

    else:
        # Use set for constant O(1) lookup
        existing_item_urls = {
            existing_item["item_url"] for existing_item in existing_items
        }

        for item in items:
            try:
                if item["item_url"] not in existing_item_urls:
                    # Validate item using Pydantic
                    document = ItemDocumentBase(
                        **item,
                        feed_id=feed_id
                    )

                    documents_to_insert.append(document.model_dump())

            except Exception as e:
                logging.warning(f"Skipping item due to error: {e}")
                continue

    if documents_to_insert:
        try:
            await documents_collection.insert_many(documents_to_insert)
            return True
        except Exception as e:
            logging.info(f"Exception {e} occurred while adding documents to the Doc Repo")
            return False

    else:
        logging.info(f"No New Documents to store!")
        return False
