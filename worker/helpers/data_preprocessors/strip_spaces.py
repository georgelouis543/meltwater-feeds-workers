def remove_leading_trailing_spaces(
        s: str
) -> str:
    return s.strip() if isinstance(s, str) else ""