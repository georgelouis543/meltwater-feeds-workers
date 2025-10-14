import datetime
import logging

import httpx


async def get_rss_response_body(
        url: str,
        render_cache_collection
) -> str:
    try:
        # Check if the source has been cached for the given URL
        is_cached = await render_cache_collection.find_one({
            "url": url,
            "is_rss_feed": True
        })
        if is_cached:
            logging.info(f"Found Cache. Returning Cached RSS Body for the URL: {url}")
            return is_cached["rss_body"]


        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()

            result = response.text

            await render_cache_collection.insert_one({
                "url": url,
                "is_rss_feed": True,
                "rss_body": result,
                "cached_at": datetime.datetime.now(datetime.UTC)
            })


            return result

    except httpx.HTTPStatusError as e:
        logging.warning(f"Could not fetch source. Exited with HTTPStatusError: {e}")
        raise e

    except httpx.RequestError as e:
        logging.warning(f"Could not fetch source. Exited with RequestError: {e}")
        raise e

    except Exception as e:
        logging.warning(f"Could not fetch source. Exited with Exception: {e}")
        raise e