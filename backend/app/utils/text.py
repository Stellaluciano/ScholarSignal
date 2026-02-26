import re


def sanitize_url(url: str) -> str:
    if not re.match(r"^https?://", url):
        return ""
    return url
