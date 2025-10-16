from datetime import datetime
import logging

def normalize_date(
        raw_date: str,
        date_regex: str | None = None
) -> str | None:
    if not raw_date or raw_date.strip() == "":
        return None

    if not date_regex or date_regex.strip() == "":
        date_regex = None

    try:
        if date_regex:
            dt = datetime.strptime(raw_date.strip(), date_regex)

        else:
            for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%b %d, %Y"):
                try:
                    dt = datetime.strptime(raw_date.strip(), fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Unknown date format for '{raw_date}'")

        return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

    except Exception as e:
        logging.warning(f"Could not parse date '{raw_date}' with format '{date_regex}': {e}")
        return None